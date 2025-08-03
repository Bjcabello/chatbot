from fastapi import FastAPI
from src.routes import chat, index
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Chatbot Viamatica")

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
def root():
    return {"message": "Chatbot Viamatica backend activo"}
