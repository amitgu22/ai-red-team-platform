from fastapi import APIRouter, HTTPException
from app.adapters.registry import list_adapters, get_adapter

router = APIRouter(prefix="/vendors", tags=["vendors"])

@router.get("")
def vendors():
    return list_adapters()

@router.get("/{name}/validate")
def validate_vendor(name: str, scenario_category: str):
    try:
        adapter = get_adapter(name)
        supported = scenario_category in adapter.capabilities or "adaptive" in adapter.capabilities
        return {"vendor": name, "scenario_category": scenario_category, "supported": supported}
    except KeyError as exc:
        raise HTTPException(404, str(exc))
