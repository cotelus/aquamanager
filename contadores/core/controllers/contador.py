from pymongo import MongoClient
from core.log.logger import logger
from core.load import get_venv

class ContadorController():
    def __init__(self, db=None):
        self.name = "Controlador de contadores - SINGLETON -"
        self.contadores = [{'nombre':'Contador 1', 'valor': 2}, {'nombre':'Contador 2', 'valor': 6}]
        self.db = db
        
        # TODO Quitar esto
        db = get_venv('CONTADORES_DB')
        self.db = db

        logger.debug("Objeto controlador de contadores creado")

    """
        Devuelve una lista de contadores
    """
    async def get_list(self):
        # return self.contadores
        await self.initialize_db()
        return await self.get_list_from_db()

    # Conexión a la base de datos
    async def initialize_db(self):
        try:
            client = MongoClient(f'mongodb://{self.db}:27017/')
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
