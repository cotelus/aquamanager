from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., gt=0, description="ID del usuario")
    username: str = Field(..., description="Nombre de usuario")
    hydrants: List[int] = Field(..., description="Lista de ID de hidrantes")
    admin: bool = Field(..., description="Indicador de administrador")

    def __init__(
        self,
        id: int = 0,
        username: str = "",
        hydrants: List[int] = [],
        admin: bool = False
    ):
        super().__init__(
            id=id,
            username=username,
            hydrants=hydrants,
            admin=admin
        )
