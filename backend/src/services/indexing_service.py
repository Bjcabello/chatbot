# backend/src/services/indexing_service.py

from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import os

def index_documents():
    folder_path = "backend/src/context"
    persist_directory = os.getenv("CHROMA_PATH", "chroma_db")

    loaders = [
        DirectoryLoader(path=folder_path, glob="**/*.md", loader_cls=TextLoader),
        DirectoryLoader(path=folder_path, glob="**/*.pdf", loader_cls=UnstructuredPDFLoader)
    ]

    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    if not documents:
        print("[INDEXACIÓN] No se encontraron documentos para indexar.")
        return

    embedding_model = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    db.persist()

    print(f"[INDEXACIÓN] {len(documents)} documentos indexados correctamente en ChromaDB.")
