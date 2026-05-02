from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from ollama import Client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    platform: str
    prompt: str

MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = Client(host=OLLAMA_HOST)

@app.get("/test")
def test():
    return {"success": True}

@app.post("/generate")
def generate(request: GenerateRequest):
    print("generating...")

    prompt_text = f"Generate a social media post for {request.platform} based on: {request.prompt}. Limit the response to 50 words."

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )

        return {
            "content": response["message"]["content"],
            "source": "ollama"
        }

    except Exception as e:
        print("Ollama failed:", e)

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt_text}]
                }
            ]
        }

        res = requests.post(url, json=payload)
        data = res.json()

        return {
            "content": data["candidates"][0]["content"]["parts"][0]["text"],
            "source": "gemini"
        }

    except Exception as e:
        print("Gemini failed:", e)

    return {
        "content": f"🚀 {request.platform} post: {request.prompt}. Stay consistent, engage your audience, and deliver value clearly! #Growth #Success",
        "source": "fallback"
    }