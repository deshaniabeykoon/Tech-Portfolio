from backend.models import Restaurant
from backend.services.llm_service import LLMFactory

class SimilarityService:
    def __init__(self):
        self.llm = LLMFactory.get_llm("together")

    def find_similar_with_twist(self, source_name: str, target_cuisine: str):
        prompt = (
            f"Find restaurants similar in vibe to '{source_name}', but serving {target_cuisine} cuisine. "
            "List 3 with one-line cultural context."
        )
        response = self.llm.generate(prompt)
        return self._parse(response)

    def _parse(self, raw):
        return [{"name": line.split("–")[0].strip(), "cultural_context": line.split("–")[1].strip()}
                for line in raw.split("\n") if "–" in line]