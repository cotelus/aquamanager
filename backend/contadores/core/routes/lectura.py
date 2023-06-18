from aiohttp.web import RouteTableDef
from aiohttp import web
import http
from core.controllers.lectura import LecturaController

def add_routes(routes: RouteTableDef):

    # Recoge las lecturas
    @routes.get('/lecturas/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')
        
        if jwt_header:
            lectura = LecturaController()
            return web.json_response(await lectura.get_list(jwt_header), status=http.HTTPStatus.OK)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)


    # Inserta una lectura
    @routes.post('/lecturas/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')
        data = await request.json()
        
        if jwt_header:
            lectura = LecturaController()
            return web.json_response(await lectura.insert_lectura(data), status=http.HTTPStatus.OK)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)
