from backend.services.llm_service import LLMFactory
import json

class ModerationService:
    def __init__(self):
        self.llm = LLMFactory.get_llm("together")

    def moderate_review(self, comment: str):
        prompt = (
            f"Analyze the following review for safety, sentiment, and toxicity.\n\n"
            f"Review: \"{comment}\"\n\n"
            f"Return JSON like:\n"
            f'{{"is_safe": true, "toxicity_level": "low", "sentiment": "positive", "flags": []}}'
        )
        response = self.llm.generate(prompt)
        try:
            return json.loads(response)
        except Exception:
            return {"is_safe": True, "toxicity_level": "low", "sentiment": "neutral", "flags": ["parse_error"]}
