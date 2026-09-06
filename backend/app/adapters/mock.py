import httpx
from .base import VendorAdapter, AdapterRequest, AdapterResult

class HTTPVendorAdapter(VendorAdapter):
    def __init__(self, name: str, capabilities: list[str], execution_modes: list[str]):
        self.name = name
        self.capabilities = set(capabilities)
        self.execution_modes = set(execution_modes)

    def validate(self, request: AdapterRequest) -> None:
        if request.scenario_category not in self.capabilities and "adaptive" not in self.capabilities:
            raise ValueError(f"{self.name} does not advertise capability '{request.scenario_category}'")
        if not request.target_endpoint:
            raise ValueError("Target endpoint is required")

    def execute(self, request: AdapterRequest) -> AdapterResult:
        self.validate(request)
        url = request.target_endpoint.rstrip("/") + "/chat"
        try:
            response = httpx.post(url, json={"message": request.prompt}, timeout=15)
            data = response.json()
            signal = bool(data.get("risk_signal"))
            return AdapterResult(
                status="COMPLETED", success=signal,
                severity=request.options.get("severity") if signal else "INFO",
                request=request.prompt, response=response.text,
                evidence={"adapter": self.name, "risk_signal": data.get("risk_signal"), "target_response": data}
            )
        except Exception as exc:
            return AdapterResult("FAILED", False, "INFO", request.prompt, "", {"adapter": self.name, "error": str(exc)})
