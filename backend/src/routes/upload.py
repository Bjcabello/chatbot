# /backend/src/routes/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from src.services.pdf_memory_indexer import index_pdfs_from_memory
from io import BytesIO

router = APIRouter()

@router.post("/upload-pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        memory_files = []

        for file in files:
            if not file.filename.endswith(".pdf"):
                raise HTTPException(status_code=400, detail=f"{file.filename} no es un archivo PDF")
            content = await file.read()
            memory_files.append(BytesIO(content))

        index_pdfs_from_memory(memory_files)

        return {"message": "PDFs indexados correctamente sin ser guardados"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
