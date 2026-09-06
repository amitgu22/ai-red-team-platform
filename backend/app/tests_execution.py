import os
from pathlib import Path
from app.adapters.command import CommandVendorAdapter
from app.adapters.base import AdapterRequest

def test_command_adapter_http_fallback(monkeypatch):
    adapter = CommandVendorAdapter("Demo", ["jailbreak"], ["batch"], "DEMO_VENDOR_COMMAND")
    monkeypatch.delenv("DEMO_VENDOR_COMMAND", raising=False)
    assert adapter.discover()["execution_backend"] == "http-fallback"

def test_command_template_writes_prompt_and_captures_output(tmp_path, monkeypatch):
    adapter = CommandVendorAdapter("Demo", ["jailbreak"], ["batch"], "DEMO_VENDOR_COMMAND")
    output = tmp_path / "result.json"
    cmd = "printf vendor-output > {output_file}; printf vendor-ok"
    monkeypatch.setenv("DEMO_VENDOR_COMMAND", cmd)
    req = AdapterRequest("http://target", "JB-001", "jailbreak", "secret prompt", 1, {"artifact_dir": str(tmp_path)})
    result = adapter.execute(req)
    assert result.status == "COMPLETED"
    assert result.success is True
    assert result.evidence["backend"] == "cli"
    assert "vendor-ok" in result.response
    assert (tmp_path / "output-demo-1.json").exists()
