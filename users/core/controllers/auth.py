
from core.log.logger import logger
from pymongo import MongoClient
import aiohttp
from aiohttp_jwt import JWTMiddleware, login_required
import jwt
from aiohttp import web
from core.load import get_venv

SECRET_KEY = 'secreto'

class AuthController():

    _instance = None
    db_name: str
    db: MongoClient
    name: str

    def __new__(cls, db_name=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.name = "Controlador de autenticación"
            cls._instance.db_name = db_name
            cls._instance.db = None
            logger.debug("Objeto controlador de autenticación creado como Singleton")
        return cls._instance
    
    @classmethod
    def delete_instance(cls):
        cls._instance = None

    async def signup(self, username: str, password: str):
        pass

    # Login de usuario
    async def login(self, username: str, password: str):
        # Realiza la autenticación y verifica las credenciales del usuario
        # Si las credenciales son válidas, genera el token JWT
        user = await self.get_user_from_db(username)
        logger.debug(f"Usuario: {user}")
        db_username = user['username']
        db_password = user['password']
        is_admin = user['admin']
        if db_username == 'admin' and str(password) == str(db_password) and is_admin:
            token = self.generate_token(username)
            return {"token":token}

        raise web.HTTPUnauthorized()

    def generate_token(self, username):
        payload = {'username': username}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    
    # Conexión a la base de datos
    async def initialize_db(self):
        try:
            client = MongoClient(f'mongodb://{self.db_name}:27017/')
            logger.debug(f"Client: {client}")
            self.db = client['db']
            logger.debug(f"Base de datos: {self.db}")
        except Exception as e:
            logger.error(f"Falló la conexión con la base de datos - {e}")

    # Rescatar usuario de la base de datos
    async def get_user_from_db(self, username: str):
        if self.db is None:
            await self.initialize_db()

        logger.debug(f"Asking to users db for {username}")
        await self.initialize_db()
        user = None
        logger.debug(f"self.db = {self.db}")

        if self.db is None:
            return None

        try:
            collection = self.db['usuarios']
            result = collection.find({"username": username})
            logger.debug(result.__dict__)

            if not result._Cursor__empty:
                for db_user in result:
                    user = {'username': db_user['username'], 'password': db_user['password'], 'admin': db_user['admin']}
                    break
            return user
        except Exception as e:
            logger.error(f"Error al consultar DB - {e}")
            return None

