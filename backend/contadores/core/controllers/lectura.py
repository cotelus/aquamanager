from influxdb import InfluxDBClient
from pymongo import MongoClient
from core.log.logger import logger
from core.load import get_venv
from influxdb import InfluxDBClient
from core.models.lectura import Lectura

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
    

    def initialize_db(self):
        if self.db is None and self.db_name != "":
            try:
                self.db = InfluxDBClient(host=self.db_name, port=8086)
                self.db.create_database('lecturas')
                self.db.switch_database('lecturas')
            except Exception as e:
                logger.error(f"Falló la conexión con la base de datos - {e}")

    def save_lectura(self, lectura: Lectura):
        json_body = [
            {
                "measurement": "lectura",
                "tags": {
                    "hidrante_id": lectura.hidrante_id,
                    "user_id": lectura.user_id
                },
                "time": lectura.fecha.isoformat(),
                "fields": {
                    "valor": lectura.valor
                }
            }
        ]
        self.db.write_points(json_body)
