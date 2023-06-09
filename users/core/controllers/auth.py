
from core.log.logger import logger
import aiohttp
from aiohttp_jwt import JWTMiddleware, login_required
import jwt
from aiohttp import web

SECRET_KEY = 'secreto'

class AuthController():

    def __init__(self, db=None):
        self.name = "Controlador de autenticacion - SINGLETON -"
        self.contadores = [{'nombre':'Contador 1', 'valor': 2}, {'nombre':'Contador 2', 'valor': 6}]
        self.db = db
        logger.debug("Objeto controlador de contadores creado")

    async def signup(self, username: str, password: str):
        pass

    async def login(self, username: str, password: str):
        # Realiza la autenticación y verifica las credenciales del usuario
        # Si las credenciales son válidas, genera el token JWT
        if username == 'admin' and password == 'admin_password':
            token = self.generate_token(username)
            return token

        raise web.HTTPUnauthorized()

    def generate_token(self, username):
        payload = {'username': username}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
