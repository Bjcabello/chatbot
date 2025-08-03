from fastapi import FastAPI
from src.routes import chat, index
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Chatbot Viamatica")




# Incluir rutas
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(index.router, prefix="/api/index", tags=["Index"])

@app.get("/")
def root():
    return {"message": "Chatbot Viamatica backend activo"}
