from datetime import datetime
from pydantic import BaseModel, Field


class Lectura(BaseModel):
    fecha: datetime = Field(..., description="Fecha de la lectura")
    valor: float = Field(..., ge=0, description="Valor de la lectura")
    hidrante_id: int = Field(..., gt=0, description="ID del hidrante")
    user_id: int = Field(..., gt=0, description="ID del usuario")

    def __init__(
        self,
        fecha: datetime = datetime.now(),
        valor: float = 0.0,
        hidrante_id: int = 0,
        user_id: int = 0
    ):
        super().__init__(
            fecha=fecha,
            valor=valor,
            hidrante_id=hidrante_id,
            user_id=user_id
        )

    def to_dict(self):
        returned_dict = self.dict()
        returned_dict['fecha'] = self.fecha.strftime("%d/%m/%Y, %H:%M:%S")
        return returned_dict
