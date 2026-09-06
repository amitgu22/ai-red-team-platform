from app.adapters.registry import get_adapter, list_adapters

def test_builtin_vendor_registry():
    names = {x["name"] for x in list_adapters()}
    assert {"Promptfoo", "PyRIT", "Garak", "Striker"} <= names
    assert "prompt-injection" in get_adapter("Promptfoo").capabilities
