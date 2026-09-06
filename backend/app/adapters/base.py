from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AdapterRequest:
    target_endpoint: str
    scenario_key: str
    scenario_category: str
    prompt: str
    attempt: int
    options: dict[str, Any] = field(default_factory=dict)

@dataclass
class AdapterResult:
    status: str
    success: bool | None
    severity: str | None
    request: str
    response: str
    evidence: dict[str, Any] = field(default_factory=dict)

class VendorAdapter(ABC):
    name: str
    capabilities: set[str] = set()
    execution_modes: set[str] = set()

    @abstractmethod
    def validate(self, request: AdapterRequest) -> None:
        pass

    def discover(self) -> dict[str, Any]:
        return {"name": self.name, "capabilities": sorted(self.capabilities), "execution_modes": sorted(self.execution_modes)}

    @abstractmethod
    def execute(self, request: AdapterRequest) -> AdapterResult:
        pass

    def normalize(self, result: AdapterResult) -> AdapterResult:
        return result
