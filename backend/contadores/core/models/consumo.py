from datetime import datetime
from pydantic import BaseModel, Field

class Consumo(BaseModel):
    fecha_inicial: float = Field(..., description="Fecha de la lectura inicial")
    fecha_final: float = Field(..., description="Fecha de la lectura final")
    valor_inicial: float = Field(..., ge=0, description="Valor lectura inicial")
    valor_final: float = Field(..., ge=0, description="Valor lectura final")
    id_hidrante: int = Field(..., gt=0, description="ID del hidrante")
    nombre_hidrante: str = Field(..., description="Nombre del hidrante")
    valor: float = Field(..., ge=0, description="Valor del consumo")

    def __init__(
        self,
        fecha_inicial: float,
        fecha_final: float,
        valor_inicial: float,
        valor_final: float,
        id_hidrante: int,
        nombre_hidrante: str,
        valor: float,
    ):
        super().__init__(
            fecha_inicial=fecha_inicial,
            fecha_final=fecha_final,
            valor_inicial=valor_inicial,
            valor_final=valor_final,
            id_hidrante=id_hidrante,
            nombre_hidrante=nombre_hidrante,
            valor=valor,
        )

    def to_dict(self):
        returned_dict = self.dict()
        returned_dict['fecha_inicial'] = datetime.fromtimestamp(self.fecha_inicial).strftime("%d/%m/%Y, %H:%M:%S")
        returned_dict['fecha_final'] = datetime.fromtimestamp(self.fecha_final).strftime("%d/%m/%Y, %H:%M:%S")
        return returned_dict
