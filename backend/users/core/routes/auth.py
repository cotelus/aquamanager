from aiohttp.web import RouteTableDef
from aiohttp import web
from core.controllers.auth import AuthController
import http

def add_routes(routes: RouteTableDef):
    """
        Devuelve si el login ha funcionado o no
    """
    @routes.post('/login/')
    async def list_(request: web.Request):
        data = await request.json()
        username = data.get('username')
        password = data.get('password')
        auth = AuthController()

        return web.json_response(
            await auth.login(username, password), status=http.HTTPStatus.ACCEPTED
        )
    
    @routes.get('/decryptjwt/')
    async def list_(request: web.Request):
        data = await request.json()
        jwt = data.get('jwt')
        auth = AuthController()

        return web.json_response(
            await auth.decrypt_jwt(jwt), status=http.HTTPStatus.OK
        )
    
    @routes.get('/users/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')

        if jwt_header:
            usuarios = AuthController()
            return web.json_response(await usuarios.get_list(jwt_header), status=http.HTTPStatus.OK)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)