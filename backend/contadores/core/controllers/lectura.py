from datetime import datetime
from influxdb import InfluxDBClient
from core.log.logger import logger
from influxdb import InfluxDBClient
from core.models.lectura import Lectura
from aiohttp import web
from core.tools import decrypt_jwt
from core.controllers.hidrante import HydrantController
from dateutil import parser

class LecturaController:
    _instance = None
    db_name: str
    db: InfluxDBClient
    name: str

    def __new__(cls, db_name=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.db_name = db_name
            cls._instance.db = None
            logger.debug("Objeto controlador de Hidrantes creado como Singleton")
        return cls._instance
    
    @classmethod
    def delete_instance(cls):
        cls._instance = None

    async def initialize_db(self):
        if self.db is None and self.db_name != "":
            try:
                self.db = InfluxDBClient(host=self.db_name, port=8086)
                self.db.create_database('lecturas')
                self.db.switch_database('lecturas')
            except Exception as e:
                logger.error(f"Falló la conexión con la base de datos - {e}")

        # Devuelve una lista de contadores
    async def get_list(self, jwt_header: str):
        user = await decrypt_jwt(jwt_header)
        if user is not None:
            lecturas_list = list()
            db_list = await self.get_list_from_db(user['user_id'], user['admin'])
            for lectura in db_list.get_points():
                lectura_model = Lectura(
                    fecha = parser.parse(lectura['time']).timestamp(),
                    valor = lectura['valor'],
                    hidrante_id = lectura['hidrante_id'],
                    user_id = lectura['user_id'],
                )
                lecturas_list.append(lectura_model.to_dict())
            return {'result': lecturas_list}
        else:
            raise web.HTTPForbidden(reason="El usuario no tiene suficientes privilegios")



    # Comprueba los datos y luego los inserta en la bd
    async def insert_lectura(self, jwt_header: str, **kwargs):
        user = await decrypt_jwt(jwt_header)
        if user is not None and user['admin']:
            required_fields = {'fecha', 'valor', 'hidrante_id', 'user_id'}
            missing_fields = required_fields - set(kwargs.keys())
            if missing_fields:
                raise web.HTTPBadRequest(reason=f"Campos requeridos: {missing_fields}")

            lectura = Lectura(
                kwargs['fecha'],
                kwargs['valor'],
                kwargs['hidrante_id'],
                kwargs['user_id']
            )
            await self.save_lectura(lectura)
        else:
            raise web.HTTPForbidden(reason="El usuario no tiene suficientes privilegios")

    # Inserta una lectura en la bd
    async def save_lectura(self, lectura: Lectura):
        await self.initialize_db()

        json_body = [
            {
                "measurement": "lectura",
                "tags": {
                    "hidrante_id": lectura.hidrante_id,
                    "user_id": lectura.user_id
                },
                "time": datetime.fromtimestamp(lectura.fecha).isoformat(),
                "fields": {
                    "valor": lectura.valor
                }
            }
        ]
        self.db.write_points(json_body)


    # Rescatar elementos de la base de datos
    async def get_list_from_db(self, id: int, admin: bool):
        await self.initialize_db()

        query = "SELECT * FROM lectura"
        if not admin:
            query = f'SELECT * FROM lectura WHERE "user_id" = {id}'


        try:
            result = self.db.query(query=query)
            return result
        except Exception as e:
            logger.error(f"Error al consultar InfluxDB - {e}")
            return []

    # Edita una lectura 
    async def edit_reading(self, jwt_header: str, **kwargs):
        user = await decrypt_jwt(jwt_header)
        if user is not None and user['admin']:
            required_fields = {'fecha', 'valor', 'hidrante_id', 'user_id'}
            missing_fields = required_fields - set(kwargs.keys())
            if missing_fields:
                raise web.HTTPBadRequest(reason=f"Campos requeridos: {missing_fields}")

            lectura = Lectura(
                fecha=kwargs['fecha'],
                valor=kwargs['valor'],
                hidrante_id=kwargs['hidrante_id'],
                user_id=kwargs['user_id']
            )

            await self.update_reading_db(lectura)

    # Edita una lectura en la BD
    async def update_reading_db(self, lectura: Lectura):
        await self.initialize_db()

        json_body = [
            {
                "measurement": "lectura",
                "tags": {
                    "hidrante_id": lectura.hidrante_id,
                    "user_id": lectura.user_id
                },
                "time": datetime.fromtimestamp(lectura.fecha).isoformat(),
                "fields": {
                    "valor": lectura.valor
                }
            }
        ]
        self.db.write_points(json_body)

    # Elimina una lectura
    async def delete_reading(self, jwt_header: str, **kwargs):
        user = await decrypt_jwt(jwt_header)
        if user is not None and user['admin']:
            required_fields = {'fecha', 'valor', 'hidrante_id', 'user_id'}
            missing_fields = required_fields - set(kwargs.keys())
            if missing_fields:
                raise web.HTTPBadRequest(reason=f"Campos requeridos: {missing_fields}")

            lectura = Lectura(
                fecha=kwargs['fecha'],
                valor=kwargs['valor'],
                hidrante_id=kwargs['hidrante_id'],
                user_id=kwargs['user_id']
            )
            await self.delete_reading_db(lectura)
        
        raise web.HTTPForbidden(reason="El usuario no tiene suficientes privilegios")

    # Elimina la lectura en la BD
    async def delete_reading_db(self, lectura: Lectura):
        await self.initialize_db()

        query = f'DELETE FROM lectura WHERE "hidrante_id" = \'{lectura.hidrante_id}\' AND "user_id" = \'{lectura.user_id}\' AND time = \'{datetime.fromtimestamp(lectura.fecha).isoformat()}\''

        try:
            self.db.query(query=query)
        except Exception as e:
            logger.error(f"Error borrando lectura influxdb - {e}")
            raise web.HTTPInternalServerError(reason="Error borrando la lectura BD")
