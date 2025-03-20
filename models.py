from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class Usuario(BaseModel):
    id: Optional[UUID] = None
    username: str
    password: str
    email: Optional[str] = None

class Dispositivo(BaseModel):
    id: Optional[UUID] = None
    nombre: str
    active: bool = False
    usuario_id: Optional[UUID] = None


class Registro(BaseModel):
    id: Optional[UUID] = None
    fecha: datetime
    coordenadas: str
    dispositivo_id: UUID
