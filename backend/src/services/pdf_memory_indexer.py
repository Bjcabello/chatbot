from typing import List
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdfminer.high_level import extract_text
from io import BytesIO
import os

def index_pdfs_from_memory(files: List[BytesIO]):
    all_docs = []

    # Extraer texto de cada PDF
    for file in files:
        text = extract_text(file)
        doc = Document(page_content=text, metadata={"source": "upload"})
        all_docs.append(doc)

    # Dividir documentos
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_split = splitter.split_documents(all_docs)

    # Crear embeddings
    embedding = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    vectordb = Chroma.from_documents(
        documents=docs_split,
        embedding=embedding,
        persist_directory=os.getenv("CHROMA_PATH", "chroma_db")
    )

    vectordb.persist()
