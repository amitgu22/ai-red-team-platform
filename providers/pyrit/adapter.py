class PyRITProvider:
    name = "pyrit"
    capabilities = ["jailbreak", "prompt-injection", "adaptive", "multi-turn"]

    def validate(self, config):
        return True

    def health_check(self):
        return {"status": "ready"}

    def execute(self, test):
        raise NotImplementedError("Wire PyRIT execution in Phase 2.")

    def parse_results(self, raw_result):
        raise NotImplementedError("Wire result normalization in Phase 2.")
