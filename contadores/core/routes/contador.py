from aiohttp.web import RouteTableDef
from aiohttp import web

from core.controllers.contador import ContadorController

def add_routes(routes: RouteTableDef):

    """
        Devuelve una lista de contadores
    """
    @routes.get('/contadores/')
    async def list_(request: web.Request):
        contador = ContadorController(db=1)
        return web.json_response(await contador.get_list(
        ), status=200)
