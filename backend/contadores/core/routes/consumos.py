from aiohttp.web import RouteTableDef
from aiohttp import web
import http

from core.controllers.consumos import ConsumptionController

def add_routes(routes: RouteTableDef):

    # Devuelve un consumo
    @routes.post('/consumos/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')
        data = None

        try:
            data = await request.json()
        except:
            return web.Response(text='La petición necesita cuerpo', status=http.HTTPStatus.NOT_ACCEPTABLE)
        
        if jwt_header:
            consumos = ConsumptionController()
            return web.json_response(await consumos.get_consumption(jwt_header, **data), status=http.HTTPStatus.OK)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)
