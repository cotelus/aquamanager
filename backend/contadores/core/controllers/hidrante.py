import random
from pymongo import MongoClient
from core.log.logger import logger
from core.load import get_venv
from pymongo.database import Database
from core.models.hidrante import Hidrante
from core.tools import decrypt_jwt
from aiohttp import web

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
    
    # Devuelve una lista de contadores
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
    
    # Devuelve un hidrante en función de su id
    async def get_hydrant(self, hydrant_id: int):
        await self.initialize_db()

        fields = {
            '_id': False,  # Excluir el campo '_id'
            'id': True,
            'valve_open': True,
            'user_id': True,
            'counter': True,
            'topic': True,
            'name': True,
        }

        collection = self.db['hidrantes']
        hydrant = collection.find_one({"id": hydrant_id}, fields)
        if hydrant:
            return Hidrante(**hydrant)
        else:
            return None

    # Inicializa las colecciones de la base de datos
    async def initialize_db_collections(self):
        logger.debug("Inicializando colecciones DB")
        if 'hidrantes' not in self.db.list_collection_names():
            self.db.create_collection('hidrantes')
            logger.debug("Se creó la colección 'hidrantes'")

    # Rescatar elementos de la base de datos
    async def get_list_from_db(self, id: int, admin: bool):
        await self.initialize_db()

        fields = {
            '_id': False,  # Excluir el campo '_id'
            'id': True,
            'valve_open': True,
            'user_id': True,
            'counter': True,
            'topic': True,
            'name': True,
        }

        query = {}
        if not admin:
            query = {"user_id": id}

        try:
            collection = self.db['hidrantes']
            result = collection.find(query, fields)
            logger.debug(result.__dict__)
            return result
        except Exception as e:
            logger.error(f"Error al consultar DB - {e}")
            return []
        
    async def get_valid_id(self) -> int:
        new_id = random.randint(1,1000000)

        while (True):
            try:
                await self.get_hydrant(new_id)
                new_id = random.randint(1,1000000)
            except:
                return new_id

    # Insertar un nuevo hidrante
    async def insert_hydrant(self, jwt_header: str, **kwargs):
        user = await decrypt_jwt(jwt_header)

        if user is not None:
            required_fields = {'topic', 'user_id', 'name'}
            missing_fields = required_fields - set(kwargs.keys())
            if missing_fields:
                raise web.HTTPBadRequest(reason=f"Campos requeridos: {missing_fields}")
           
            # Comprobar valores opcionales modelo
            counter = 0
            valve_open = False
            if 'counter' in kwargs:
                counter = kwargs['counter']
            if 'valve_open' in kwargs:
                valve_open = kwargs['valve_open']

            # Obtener un id de hidrante válido
            new_id = self.get_valid_id()

            hydrant = Hidrante(
                id=new_id,
                topic = kwargs['topic'],
                user_id = kwargs['user_id'],
                name = kwargs['name'],
                valve_open = valve_open,
                counter = counter
            )
            await self.insert_hydrant_db(hydrant)
            return {
                "result": hydrant.to_dict(),
                "message": f"Hidrante {new_id} creado con exito"
            }
        
    # Inserta un documento de hidrante
    async def insert_hydrant_db(self, hydrant: Hidrante):
        await self.initialize_db()

        collection = self.db['hidrantes']
        collection.insert_one(hydrant.to_dict())

    # Edita un hidrante existente
    async def edit_hydrant(self, jwt_header: str, hydrant_id: int, **kwargs):
        user = await decrypt_jwt(jwt_header)

        if user is not None:
            hydrant = await self.get_hydrant(hydrant_id)
            if hydrant:
                if not user['admin'] or hydrant.user_id != user['id']:
                    raise web.HTTPForbidden(reason="El usuario no tiene suficientes privilegios")

                updated_hydrant = hydrant.copy(update=kwargs)
                await self.update_hydrant_db(updated_hydrant)
                return updated_hydrant
            else:
                raise web.HTTPNotFound(reason=f"El hidrante con id:{hydrant_id} no existe")
        else:
            raise web.HTTPForbidden(reason="El usuario no tiene suficientes privilegios")

    # Actualiza un documento de hidrante
    async def update_hydrant_db(self, hydrant: Hidrante):
        await self.initialize_db()

        collection = self.db['hidrantes']
        collection.update_one({"id": hydrant.id}, {"$set": hydrant.dict(exclude={"id"})})

    # Eliminar un hidrante
    async def delete_hydrant(self,  jwt_header: str, hydrant_id: int):
        user = await decrypt_jwt(jwt_header)

        if user is not None:
            hydrant = await self.get_hydrant(hydrant_id)
            if hydrant:
                await self.delete_hydrant_db(hydrant.id)
                return {"result": f"Hidrante con id: {hydrant.id} eliminado"}
            else:
                raise web.HTTPNotFound(reason=f"El hidrante con id:{hydrant_id} no existe")
            
    # Eliminaun documento de hidrante
    async def delete_hydrant_db(self, hydrant_id: int):
        await self.initialize_db()

        collection = self.db['hidrantes']
        collection.delete_one({"id": hydrant_id})
    