from fastapi import FastAPI
from pydantic import BaseModel
import os
from ollama import Client

app = FastAPI()

class GenerateRequest(BaseModel):
    platform: str
    prompt: str

MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

client = Client(host=OLLAMA_HOST)

@app.get("/test")
def test():
    return {"success": True}

@app.post("/generate")
def generate(request: GenerateRequest):
    print("generating...")

    prompt_text = f"Generate a social media post for {request.platform} based on: {request.prompt}. Limit the response to 50 words."

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )

    return {
        "content": response["message"]["content"]
    }