from fastapi import APIRouter, HTTPException
from src.models.chat import Chat
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import os

router = APIRouter()

@router.post("/")
def responder(chat: Chat):
    try:
        persist_directory = os.getenv("CHROMA_PATH", "chroma_db")

        # Configurar el modelo de embeddings
        embedding_model = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )

        # Cargar la base vectorial de Chroma
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model
        )
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        # Prompt personalizado
        prompt_usuario = (
            f"Usuario: {chat.usuario} (DNI: {chat.dni}, Rol: {chat.tipo_usuario})\n"
            f"Pregunta: {chat.pregunta}\n"
            "Responde como un asistente especializado en procesos empresariales de Viamatica, "
            "usando únicamente los documentos indexados. No respondas si no tienes contexto. Sé claro y preciso."
        )

        # Modelo LLM (Ollama + Mistral)
        llm = Ollama(model="mistral")

        # Cadena QA
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        resultado = qa.invoke(prompt_usuario)

        return {
            "respuesta": resultado["result"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
