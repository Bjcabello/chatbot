from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  

app = FastAPI()
app.title = "ChatBot IA"

@app.get("/")
def read_root():
    return {"message": "ChatBot Viamatica API funcionando"}
