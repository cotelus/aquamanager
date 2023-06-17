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
        contador = HydrantController()
        return web.json_response(await contador.get_list(
        ), status=http.HTTPStatus.OK)
