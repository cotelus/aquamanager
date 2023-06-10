
from core.log.logger import logger
from pymongo import MongoClient
import aiohttp
from aiohttp_jwt import JWTMiddleware, login_required
import jwt
from aiohttp import web
from core.load import get_venv

SECRET_KEY = 'secreto'

class AuthController():

    def __init__(self, db=None):
        self.name = "Controlador de autenticacion - SINGLETON -"
        self.contadores = [{'nombre':'Contador 1', 'valor': 2}, {'nombre':'Contador 2', 'valor': 6}]
        self.db = db

        # TODO Quitar esto
        db = get_venv('AUTH_DB')
        self.db = db

        logger.debug("Objeto controlador de contadores creado")

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
            return token

        raise web.HTTPUnauthorized()

    def generate_token(self, username):
        payload = {'username': username}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    
    # Conexión a la base de datos
    async def initialize_db(self):
        try:
            client = MongoClient(f'mongodb://{self.db}:27017/')
            logger.debug(f"Client: {client}")
            self.db = client['db']
            logger.debug(f"Base de datos: {self.db}")
        except Exception as e:
            logger.error(f"Falló la conexión con la base de datos - {e}")

    # Rescatar usuario de la base de datos
    async def get_user_from_db(self, username: str):
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

