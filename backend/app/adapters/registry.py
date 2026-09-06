from .command import CommandVendorAdapter

BUILTIN_ADAPTERS = {
    "Promptfoo": CommandVendorAdapter("Promptfoo", ["jailbreak", "prompt-injection", "data-leakage"], ["batch"], "PROMPTFOO_COMMAND"),
    "PyRIT": CommandVendorAdapter("PyRIT", ["jailbreak", "prompt-injection", "adaptive", "multi-turn"], ["batch", "adaptive", "multi-turn"], "PYRIT_COMMAND"),
    "Garak": CommandVendorAdapter("Garak", ["jailbreak", "prompt-injection", "data-leakage", "hallucination"], ["batch"], "GARAK_COMMAND"),
    "Striker": CommandVendorAdapter("Striker", ["prompt-injection", "agent", "tool-abuse"], ["batch", "agent"], "STRIKER_COMMAND"),
}

def get_adapter(name: str):
    adapter = BUILTIN_ADAPTERS.get(name)
    if not adapter:
        raise KeyError(f"No adapter registered for provider '{name}'")
    return adapter

def list_adapters():
    return [a.discover() for a in BUILTIN_ADAPTERS.values()]
