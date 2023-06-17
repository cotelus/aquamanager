from datetime import datetime
from pydantic import BaseModel, Field

class Hidrante(BaseModel):
    id: int = Field(..., description="ID del hidrante")
    valve_open: bool = Field(..., description="Indicador de si la válvula está abierta")
    counter: float = Field(..., ge=0, description="Contador del hidrante")
    topic: str = Field(..., description="Tópico del hidrante")
    user_id: int = Field(..., gt=0, description="ID del usuario")

    def __init__(
        self,
        id: int,
        valve_open: bool,
        counter: float,
        topic: str,
        user_id: int
    ):
        super().__init__(
            id=id,
            valve_open=valve_open,
            counter=counter,
            topic=topic,
            user_id=user_id
        )

    def to_dict(self):
        return self.dict()
