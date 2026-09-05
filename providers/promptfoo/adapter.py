class PromptfooProvider:
    name = "promptfoo"
    capabilities = ["jailbreak", "prompt-injection", "data-leakage"]

    def validate(self, config):
        return True

    def health_check(self):
        return {"status": "ready"}

    def execute(self, test):
        raise NotImplementedError("Wire Promptfoo execution in Phase 2.")

    def parse_results(self, raw_result):
        raise NotImplementedError("Wire result normalization in Phase 2.")
