from .mock import HTTPVendorAdapter

BUILTIN_ADAPTERS = {
    "Promptfoo": HTTPVendorAdapter("Promptfoo", ["jailbreak", "prompt-injection", "data-leakage"], ["batch"]),
    "PyRIT": HTTPVendorAdapter("PyRIT", ["jailbreak", "prompt-injection", "adaptive", "multi-turn"], ["batch", "adaptive", "multi-turn"]),
    "Garak": HTTPVendorAdapter("Garak", ["jailbreak", "prompt-injection", "data-leakage", "hallucination"], ["batch"]),
    "Striker": HTTPVendorAdapter("Striker", ["prompt-injection", "agent", "tool-abuse"], ["batch", "agent"]),
}

def get_adapter(name: str):
    adapter = BUILTIN_ADAPTERS.get(name)
    if not adapter:
        raise KeyError(f"No adapter registered for provider '{name}'")
    return adapter

def list_adapters():
    return [a.discover() for a in BUILTIN_ADAPTERS.values()]
