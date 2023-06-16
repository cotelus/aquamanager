from pymongo import MongoClient
from core.log.logger import logger
from core.load import get_venv

class LecturaController:
    _instance = None
    db_name: str
    db: MongoClient
    name: str

    def __new__(cls, db_name=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.name = "Controlador de contadores"
            cls._instance.db_name = db_name
            cls._instance.db = None
            logger.debug("Objeto controlador de autenticación creado como Singleton")
        return cls._instance

    @classmethod
    def delete_instance(cls):
        cls._instance = None

    # Devuelve una lista de lecturas
    async def get_list(self, filter:str):
        await self.initialize_db()
        return await self.get_list_from_db()

    # Conexión a la base de datos
    async def initialize_db(self):
        try:
            client = MongoClient(f'mongodb://{self.db_name}:27017/')
            logger.debug(f"Client: {client}")
            self.db = client['db']
            logger.debug(f"Base de datos: {self.db}")
        except Exception as e:
            logger.error(f"Falló la conexión con la base de datos - {e}")

    # Rescatar elementos de la base de datos
    async def get_list_from_db(self):
        logger.debug(f"self.db = {self.db}")

        if self.db is None:
            return []

        try:
            collection = self.db['contadores']
            result = collection.find()
            logger.debug(result.__dict__)
            contadores = [{'nombre': contador['nombre'], 'valor': contador['valor']} for contador in result]
            return contadores
        except Exception as e:
            logger.error(f"Error al consultar DB - {e}")
            return []
