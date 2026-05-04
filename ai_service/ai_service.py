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

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY","AIzaSyA5mCaRs4w6H2V2eZwJ_fWw4-d6ueOTD9g")

client = Client(host=OLLAMA_HOST)

@app.get("/test")
def test():
    return {"success": True}


MICROSERVICE_URL = os.getenv("MICROSERVICE_URL", "https://ai-api-five-sigma.vercel.app/generate")

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
        res = requests.post(
            MICROSERVICE_URL,
            json={"prompt": prompt_text},
            timeout=60
        )

        data = res.json()

        return {
            "content": data.get("output", f"🚀 {request.platform} post: {request.prompt}. Stay consistent, engage your audience, and deliver value clearly! #Growth #Success"),
            "source": "node_microservice"
        }

    except Exception as e:
        print("Microservice failed:", e)

    return {
        "content": f"🚀 {request.platform} post: {request.prompt}. Stay consistent, engage your audience, and deliver value clearly! #Growth #Success",
        "source": "fallback"
    }