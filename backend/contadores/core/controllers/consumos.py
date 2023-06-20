from core.log.logger import logger
from core.models.hidrante import Hidrante
from core.tools import decrypt_jwt
from aiohttp import web
from core.controllers.hidrante import HydrantController
from core.controllers.lectura import LecturaController
from core.models.consumo import Consumo
from datetime import datetime

class ConsumptionController():
    _instance = None
    name: str

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            logger.debug("Objeto controlador de Consumos creado como Singleton")
        return cls._instance
    
    @classmethod
    def delete_instance(cls):
        cls._instance = None

    # Devuelve un consumo
    async def get_consumption(self, jwt_header:str, **kwargs):
        user = await decrypt_jwt(jwt_header)
        if user is not None and user['admin']:
            required_fields = {'fecha_inicial', 'fecha_final', 'nombre_hidrante'}
            missing_fields = required_fields - set(kwargs.keys())
            if missing_fields:
                raise web.HTTPBadRequest(reason=f"Campos requeridos: {missing_fields}")
            
            fecha1 = kwargs['fecha_inicial'] / 1000
            fecha2 = kwargs['fecha_final'] / 1000
            if fecha1 > fecha2:
                fecha1 = kwargs['fecha_final'] / 1000
                fecha2 = kwargs['fecha_inicial'] / 1000

            hidrante = HydrantController.get_hydrant_by_name(kwargs['nombre_hidrante'])
            if hidrante is not None:
                valor_inicial = LecturaController.get_closest_reading(fecha1, hidrante.id)
                valor_final = LecturaController.get_closest_reading(fecha2, hidrante.id)

                consumo = Consumo(
                    fecha1,
                    fecha2,
                    valor_inicial.valor,
                    valor_final.valor,
                    hidrante.id,
                    hidrante.nombre,
                    valor_final.valor - valor_inicial.valor
                )
                return {"result": consumo.to_dict()}
            else:
                return web.HTTPNotFound(reason=f"Hidrante: {kwargs['nombre_hidrante']} no existe")

            
        

    async def get_list(self, jwt_header: str):
        user = await decrypt_jwt(jwt_header)
        if user is not None:
            hydrant_list = list()
            db_list = await self.get_list_from_db(user['user_id'], user['admin'])
            for hydrant in db_list:
                hydrant_model = Hidrante(
                    id = hydrant['id'],
                    valve_open = hydrant['valve_open'],
                    counter = hydrant['counter'],
                    topic = hydrant['topic'],
                    user_id = hydrant['user_id'],
                    name = hydrant['name'],
                )
                hydrant_list.append(hydrant_model.to_dict())
            return {'result': hydrant_list}
        else:
            raise web.HTTPForbidden(reason="El usuario no tiene suficientes privilegios")
