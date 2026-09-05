from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProviderCreate(BaseModel):
    name: str
    provider_type: str = "container"
    version: Optional[str] = None
    image: Optional[str] = None
    capabilities: list[str] = []
    execution_modes: list[str] = []


class ProviderRead(ProviderCreate):
    id: int
    enabled: bool
    model_config = ConfigDict(from_attributes=True)


class TargetCreate(BaseModel):
    name: str
    target_type: str
    endpoint: str
    capabilities: list[str] = []
    description: Optional[str] = None


class TargetRead(TargetCreate):
    id: int
    enabled: bool
    model_config = ConfigDict(from_attributes=True)
