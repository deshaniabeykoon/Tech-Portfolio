import os
import json
import requests
from together import Together
from huggingface_hub import InferenceClient
from abc import ABC, abstractmethod

# Load environment variables
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
DEESEEK_API_KEY = os.getenv("DEESEEK_API_KEY")


# Abstract Base Class
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


# OpenAI mock (if needed later)
class OpenAIProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        return f"[MOCK GPT RESPONSE] Traditional dishes for: {prompt}"


# DeepSeek via DeepSeek API (optional)
class DeepSeekProvider(LLMProvider):
    def __init__(self):
        self.api_key = DEESEEK_API_KEY
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model_name = "deepseek-chat"

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "[DeepSeek ERROR] No API Key provided"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"[DeepSeek ERROR] Request failed: {e}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"[DeepSeek ERROR] Failed to parse response: {e}"


# Together-hosted DeepSeek model (recommended)
class TogetherDeepSeekProvider(LLMProvider):
    def __init__(self):
        self.api_key = TOGETHER_API_KEY
        self.model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
        self.client = Together(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a culinary cultural expert and storyteller."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Together DeepSeek ERROR] {str(e)}"


# Hugging Face Zephyr or Mistral via InferenceClient
class HuggingFaceProvider(LLMProvider):
    def __init__(self):
        self.client = InferenceClient(
            model="HuggingFaceH4/zephyr-7b-alpha",  # Or "mistralai/Mistral-7B-Instruct-v0.2"
            token=HUGGINGFACE_TOKEN
        )

    def generate(self, prompt: str) -> str:
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat_completions(messages=messages, max_new_tokens=150)
            return response.choices[0].message.content
        except Exception as e:
            return f"[HuggingFace ERROR] {str(e)}"


# Local or Mock LLaMA
class LLaMAProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        return f"[LLaMA MOCK] Response for: {prompt}"


# Factory to switch between providers
class LLMFactory:
    @staticmethod
    def get_llm(provider_name: str) -> LLMProvider:
        providers = {
            "openai": OpenAIProvider,
            "deepseek": DeepSeekProvider,
            "together": TogetherDeepSeekProvider,
            "huggingface": HuggingFaceProvider,
            "llama": LLaMAProvider,
        }
        provider_cls = providers.get(provider_name.lower())
        if not provider_cls:
            raise ValueError(f"Unknown provider: {provider_name}")
        return provider_cls()
