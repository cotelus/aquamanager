
from core.log.logger import logger
from pymongo import MongoClient
import aiohttp
from aiohttp_jwt import JWTMiddleware, login_required
import jwt
from aiohttp import web
from core.load import get_venv
from pymongo.database import Database
import bcrypt
from core.models.user import User

SECRET_KEY = 'secreto'

class AuthController():

    _instance = None
    db_name: str
    db: Database
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

    """
    Login de usuario
        1. Realiza la autenticación y verifica las credenciales del usuario
        2. Si las credenciales son válidas, genera el token JWT
    """
    async def login(self, username: str, password: str):
        user = await self.check_user_from_db(username, password)
        if user is None:
            logger.info(f"Wrong password for user: {username}")
            raise web.HTTPUnauthorized()

        logger.debug(f"Usuario: {user} loged in")
        
        # Generar el token y devolverlo
        token = await self.generate_token(user)
        return {"token":token}
    
    async def generate_token(self, user: User):
        payload = {
            'username': user.username,
            'user_id': user.id,
            'hydrants': user.hydrants,
            'admin': user.admin
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    async def decrypt_jwt(self, token_jwt: str):
        return jwt.decode(token_jwt, SECRET_KEY, algorithms=['HS256'])

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
        if 'usuarios' not in self.db.list_collection_names():
            self.db.create_collection('usuarios')
            logger.debug("Se creó la colección 'usuarios'")

    # Comprueba credenciales y devuelve al usuario
    async def check_user_from_db(self, username: str, password:str) -> User:
        user: User = None
        await self.initialize_db()

        logger.debug(f"Asking to users db for {username}")

        # Obtener el documento del usuario de la base de datos
        document = self.db.usuarios.find_one({'username': username})

        if document:
            bcrypt_pass = str(document['password'])

            # Verificar contraseña
            try:
                same_pass = bcrypt.checkpw(password.encode('utf-8'), bcrypt_pass.encode('utf-8'))
                if same_pass:
                    user = User(
                        id = document['id'],
                        username = document['username'],
                        hydrants = document['hydrants'],
                        admin = document['admin']
                    )
            except ValueError:
                logger.debug(f"Invalid password format - {username}")

        return user
