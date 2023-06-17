from pymongo import MongoClient
from core.log.logger import logger
from core.load import get_venv
from pymongo.database import Database
from core.models.hidrante import Hidrante

class HydrantController():
    _instance = None
    db_name: str
    db: Database
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

    """
        Devuelve una lista de contadores
    """
    async def get_list(self):
        # return self.contadores
        hydrant_list = list()
        db_list = await self.get_list_from_db()
        for hydrant in db_list:
            hydrant_model = Hidrante(
                id = hydrant['id'],
                valve_open = hydrant['valve_open'],
                counter = hydrant['counter'],
                topic = hydrant['topic'],
                user_id = hydrant['user_id'],
            )
            hydrant_list.append(hydrant_model.to_dict())
        return {'result': hydrant_list}

    # Conexión e inicialización de la base de datos
    async def initialize_db(self):
        if self.db is None and self.db_name != "":
            try:
                client = MongoClient(f'mongodb://{self.db_name}:27017/')
                logger.debug(f"Client: {client}")
                self.db = client['db']
                logger.debug(f"Base de datos: {self.db}")
                logger.debug(f"BD: mongodb://{self.db_name}:27017/")
                await self.initialize_db_collections()
            except Exception as e:
                logger.error(f"Falló la conexión con la base de datos - {e}")
    
    # Inicializa las colecciones de la base de datos
    async def initialize_db_collections(self):
        logger.debug("Inicializando colecciones DB")
        if 'hidrantes' not in self.db.list_collection_names():
            self.db.create_collection('hidrantes')
            logger.debug("Se creó la colección 'hidrantes'")

    # Rescatar elementos de la base de datos
    async def get_list_from_db(self):
        await self.initialize_db()

        fields = {
            '_id': False,  # Excluir el campo '_id'
            'id': True,
            'valve_open': True,
            'user_id': True,
            'counter': True,
            'topic': True
        }

        try:
            collection = self.db['hidrantes']
            result = collection.find({}, fields)
            logger.debug(result.__dict__)
            return result
        except Exception as e:
            logger.error(f"Error al consultar DB - {e}")
            return []
