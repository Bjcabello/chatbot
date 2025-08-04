from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes.chat import router as chat_router
from src.routes.upload import router as upload_router
from src.routes.index import router as index_router

from src.services.indexing_service import index_documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código al iniciar la app
    index_documents()
    yield
    # Código al cerrar la app (opcional)

app = FastAPI(lifespan=lifespan)

# Rutas
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(upload_router, prefix="/upload", tags=["Cargar PDF"])
app.include_router(index_router, prefix="/docs", tags=["Indexación manual"])
