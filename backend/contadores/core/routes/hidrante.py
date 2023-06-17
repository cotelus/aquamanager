from aiohttp.web import RouteTableDef
from aiohttp import web
import http

from core.controllers.hidrante import HydrantController

def add_routes(routes: RouteTableDef):

    """
        Devuelve una lista de contadores
    """
    @routes.get('/hidrantes/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')
        
        if jwt_header:
            contador = HydrantController()
            return web.json_response(await contador.get_list(jwt_header), status=http.HTTPStatus.OK)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)
