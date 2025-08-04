from fastapi import APIRouter
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import os

router = APIRouter()

@router.post("/index")
def index_docs():
    folder_path = "backend/src/context"  
    persist_directory = os.getenv("CHROMA_PATH", "chroma_db")

    # Cargar documentos .md y .pdf (sin guardarlos, solo para indexar)
    loaders = [
        DirectoryLoader(
            path=folder_path,
            glob="**/*.md",
            loader_cls=TextLoader
        ),
        DirectoryLoader(
            path=folder_path,
            glob="**/*.pdf",
            loader_cls=UnstructuredPDFLoader
        )
    ]

    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    # Embeddings
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # Guardar en Chroma
    db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    db.persist()

    return {"message": f"{len(documents)} documentos indexados en ChromaDB correctamente."}
