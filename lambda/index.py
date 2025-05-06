# === Step 1: FastAPI API for inference (to replace Lambda) ===

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json

# Dummy model simulation (replace with real inference logic if needed)
def infer_from_model(message: str, conversation_history: Optional[List[dict]] = None) -> dict:
    # This is where you'd connect to Bedrock or other models in real deployment
    response_text = f"Echo: {message}"
    history = conversation_history or []
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response_text})
    return {
        "success": True,
        "response": response_text,
        "conversationHistory": history
    }

# Define the FastAPI app
app = FastAPI()

class MessageRequest(BaseModel):
    message: str
    conversationHistory: Optional[List[dict]] = []

@app.post("/inference")
async def inference_api(req: MessageRequest):
    try:
        result = infer_from_model(req.message, req.conversationHistory)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

# Run with: uvicorn filename:app --reload
# For Google Colab:
# !pip install fastapi uvicorn nest_asyncio pyngrok
# import nest_asyncio
# from pyngrok import ngrok
# nest_asyncio.apply()
# public_url = ngrok.connect(8000)
# uvicorn.run(app, port=8000)


# === Step 2: Client code in Colab to call this API ===

import requests

API_URL = "http://localhost:8000/inference"  # replace with ngrok public_url if in Colab

payload = {
    "message": "こんにちは、調子はどう？",
    "conversationHistory": []
}

response = requests.post(API_URL, json=payload)
print(response.json())
