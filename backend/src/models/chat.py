from pydantic import BaseModel, Field
from typing import Literal

class Chat(BaseModel):
    usuario: str
    dni: str = Field(min_length=10, max_length=10)
    tipo_usuario: Literal['admin', 'cliente']
    pregunta: str
