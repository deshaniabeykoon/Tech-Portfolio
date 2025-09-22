# backend/routes/llm_routes.py or generation_routes.py

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal
from backend.services.llm_service import LLMFactory
from dotenv import load_dotenv
from backend.schemas import FoodFactResponse, FoodFactRequest, AboutPageRequest

load_dotenv()

router = APIRouter(prefix="/llm", tags=["LLM"])

# Request & Response Models
class LLMRequest(BaseModel):
    prompt: str = Field(..., example="Suggest traditional food from Ethiopia")
    provider: Literal["openai", "deepseek", "llama", "huggingface", "together"] = Field(default="openai", example="deepseek")

class LLMResponse(BaseModel):
    provider: str
    response: str

#@router.get("/generate", response_model=LLMResponse, summary="Generate general response using LLM")
def generate_response(
    prompt: str = Query(..., example="Suggest traditional Korean dishes"),
    provider: Literal["openai", "deepseek", "llama", "huggingface", "together"] = Query("together")
):
    """
    Returns general LLM completion from selected provider.
    """
    try:
        llm = LLMFactory.get_llm(provider)
        response = llm.generate(prompt)
        return {"provider": provider, "response": response}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "details": str(e)})

@router.post("/summarize-about-page", summary="Generate professional summary for a restaurant's About page")
def summarize_about_page(request: AboutPageRequest):
    """
    Summarizes a restaurant's About section using the selected LLM provider.
    """
    try:
        prompt = (
            f"Extract a concise, professional 1–2 sentence summary from the About Us page "
            f"for a restaurant named '{request.restaurant_name}'. "
            f"Focus on its cultural background, cuisine style, and overall experience. "
            f"Return only the summary."
        )

        llm = LLMFactory.get_llm(request.provider)
        summary = llm.generate(prompt)

        return {
            "restaurant_name": request.restaurant_name,
            "provider": request.provider,
            "summary": summary.strip()
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Failed to summarize", "details": str(e)})


#@router.post("/generate-food-fact", response_model=FoodFactResponse, summary="Generate cultural story about a food item")
def generate_cultural_fact(request: FoodFactRequest):
    """
    Uses LLM to generate a unique cultural fact or short story about a traditional food.
    """
    try:
        summary_prompt = (
            f"Provide a concise one-line short summary introducing the traditional food item: {request.food_name}."
        )

        detail_prompt = (
            f"You are a cultural food expert. Share a unique and interesting cultural fact or story "
            f"about the traditional food item: {request.food_name}. "
            f"Include its cultural significance, any festivals it's associated with, and a short fun fact if applicable. "
            f"Return this in 3-4 sentences maximum."
        )

        llm = LLMFactory.get_llm(request.provider)

        # Generate one-line summary
        summary_response = llm.generate(summary_prompt)

         # Generate detailed fact/story
        response = llm.generate(detail_prompt)

        return {
            "food_name": request.food_name,
            "provider": request.provider,
            "summary": summary_response.strip(),
            "fact": response.strip()
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "details": str(e)})