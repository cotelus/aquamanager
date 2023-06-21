from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., gt=0, description="ID del usuario")
    username: str = Field(..., description="Nombre de usuario")
    admin: bool = Field(..., description="Indicador de administrador")

    def __init__(
        self,
        id: int = 0,
        username: str = "",
        admin: bool = False
    ):
        super().__init__(
            id=id,
            username=username,
            admin=admin
        )

    def to_dict(self):
        return self.dict()
