import os
from langchain_community.document_loaders import PyPDFLoader, MarkdownLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")

def index_documents(folder_path: str):
    loaders = []

    # Cargar archivos .md
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                loaders.append(MarkdownLoader(file_path=file_path))

            elif file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                loaders.append(PyPDFLoader(file_path))

    # Cargar y dividir documentos
    documents = []
    for loader in loaders:
        docs = loader.load()
        documents.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)

    # Embeddings y persistencia
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )

    vectordb.persist()
