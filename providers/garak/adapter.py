class GarakProvider:
    name = "garak"
    capabilities = ["jailbreak", "prompt-injection", "data-leakage", "hallucination"]

    def validate(self, config):
        return True

    def health_check(self):
        return {"status": "ready"}

    def execute(self, test):
        raise NotImplementedError("Wire Garak execution in Phase 2.")

    def parse_results(self, raw_result):
        raise NotImplementedError("Wire result normalization in Phase 2.")
