import json
import os
import shlex
import subprocess
import tempfile
import time
from pathlib import Path
from .base import VendorAdapter, AdapterRequest, AdapterResult

class CommandVendorAdapter(VendorAdapter):
    """Runs a real vendor CLI when its command is configured.

    Command templates may use {prompt_file}, {target}, {scenario}, {attempt}, {output_file}.
    The prompt is written to a temporary artifact so secrets do not appear in process args.
    """
    def __init__(self, name: str, capabilities: list[str], execution_modes: list[str], env_var: str):
        self.name = name
        self.capabilities = set(capabilities)
        self.execution_modes = set(execution_modes)
        self.env_var = env_var

    def discover(self):
        data = super().discover()
        command = os.getenv(self.env_var, "").strip()
        data.update({"execution_backend": "cli" if command else "http-fallback", "configured": bool(command), "command_env": self.env_var})
        return data

    def validate(self, request: AdapterRequest) -> None:
        if request.scenario_category not in self.capabilities and "adaptive" not in self.capabilities:
            raise ValueError(f"{self.name} does not advertise capability '{request.scenario_category}'")
        if not request.target_endpoint:
            raise ValueError("Target endpoint is required")

    def execute(self, request: AdapterRequest) -> AdapterResult:
        self.validate(request)
        command = os.getenv(self.env_var, "").strip()
        if not command:
            return self._http_fallback(request)

        artifact_dir = Path(request.options.get("artifact_dir") or tempfile.mkdtemp(prefix="redteam-"))
        artifact_dir.mkdir(parents=True, exist_ok=True)
        prompt_file = artifact_dir / f"prompt-{self.name.lower()}-{request.attempt}.txt"
        output_file = artifact_dir / f"output-{self.name.lower()}-{request.attempt}.json"
        prompt_file.write_text(request.prompt, encoding="utf-8")
        values = {
            "prompt_file": shlex.quote(str(prompt_file)),
            "target": shlex.quote(request.target_endpoint),
            "scenario": shlex.quote(request.scenario_key),
            "attempt": str(request.attempt),
            "output_file": shlex.quote(str(output_file)),
        }
        rendered = command.format(**values)
        timeout = int(request.options.get("timeout_seconds", 60))
        started = time.time()
        try:
            proc = subprocess.run(rendered, shell=True, capture_output=True, text=True, timeout=timeout, check=False)
            duration_ms = int((time.time() - started) * 1000)
            response = proc.stdout[-20000:]
            evidence = {"adapter": self.name, "backend": "cli", "exit_code": proc.returncode, "duration_ms": duration_ms,
                        "stderr": proc.stderr[-5000:], "artifact_dir": str(artifact_dir)}
            if output_file.exists():
                try:
                    evidence["vendor_output"] = json.loads(output_file.read_text(encoding="utf-8"))
                except Exception:
                    evidence["vendor_output_file"] = str(output_file)
            success = proc.returncode == 0
            return AdapterResult("COMPLETED" if success else "FAILED", success, request.options.get("severity") if not success else "INFO",
                                 request.prompt, response, evidence)
        except subprocess.TimeoutExpired as exc:
            return AdapterResult("TIMEOUT", False, "INFO", request.prompt, (exc.stdout or "")[-5000:] if exc.stdout else "",
                                 {"adapter": self.name, "backend": "cli", "timeout_seconds": timeout, "artifact_dir": str(artifact_dir)})

    def _http_fallback(self, request: AdapterRequest) -> AdapterResult:
        import httpx
        url = request.target_endpoint.rstrip("/") + "/chat"
        try:
            response = httpx.post(url, json={"message": request.prompt}, timeout=int(request.options.get("timeout_seconds", 15)))
            data = response.json()
            signal = bool(data.get("risk_signal"))
            return AdapterResult("COMPLETED", signal, request.options.get("severity") if signal else "INFO", request.prompt, response.text,
                                 {"adapter": self.name, "backend": "http-fallback", "risk_signal": data.get("risk_signal"), "target_response": data})
        except Exception as exc:
            return AdapterResult("FAILED", False, "INFO", request.prompt, "", {"adapter": self.name, "backend": "http-fallback", "error": str(exc)})
