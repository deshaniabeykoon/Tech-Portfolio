from backend.services.llm_service import LLMFactory
from backend.scheduler import clean_summary

class ChatService:
    def __init__(self):
        self.llm = LLMFactory.get_llm("together")

    def respond(self, question, location="Auckland", time="now"):
        prompt = (
            f"You are a cultural food concierge.\nUser is in {location} at {time}.\n"
            f"User question: {question}\n\nAnswer concisely and culturally helpfully."
        )
        response = self.llm.generate(prompt)
        cleaned_response = clean_summary(response)
        #return self.llm.generate(prompt)
        return cleaned_response
