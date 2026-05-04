from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/socialdb")
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL","http://ai-service:5001")

app = FastAPI()

origins = [
        "http://frontend:5173",
        "http://localhost:3000"
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=False,  
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    platform: str
    prompt: str

def serialize_post(post):
    return {
        "platform": post["platform"],
        "prompt": post["prompt"],
        "content": post["content"],
        "sent": post.get("sent", False)
    }

@app.post("/generate")
async def generate_post(request: GenerateRequest):
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client_http:
        resp = await client_http.post(f"{AI_SERVICE_URL}/generate", json=request.dict())
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="AI service failed")
        content = resp.json()["content"]

    post = {
        "platform": request.platform,
        "prompt": request.prompt,
        "content": content,
        "sent": False
    }
    return serialize_post(post)
