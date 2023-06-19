from aiohttp.web import RouteTableDef
from aiohttp import web
import http

from core.controllers.hidrante import HydrantController

def add_routes(routes: RouteTableDef):

    
    # Devuelve una lista de contadores
    @routes.get('/hidrantes/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')
        
        if jwt_header:
            contador = HydrantController()
            return web.json_response(await contador.get_list(jwt_header), status=http.HTTPStatus.OK)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)
        
    # Devuelve una lista de contadores
    @routes.post('/hidrantes/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')
        data = await request.json()
        
        if jwt_header:
            contador = HydrantController()
            return web.json_response(await contador.insert_hydrant(jwt_header, **data), status=http.HTTPStatus.CREATED)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)
        
    # Devuelve una lista de contadores
    @routes.put('/hidrantes/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')
        data = await request.json()

        if not 'hydrant_id' in data:
            return web.Response(text='El id del hidrante es necesario', status=http.HTTPStatus.NOT_ACCEPTABLE)
        
        if jwt_header:
            contador = HydrantController()
            return web.json_response(await contador.edit_hydrant(jwt_header, hydrant_id=data['hydrant_id'], **data), status=http.HTTPStatus.OK)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)
        
    # Devuelve una lista de contadores
    @routes.delete('/hidrantes/')
    async def list_(request: web.Request):
        jwt_header = request.headers.get('Authorization')
        data = await request.json()
        if not 'hydrant_id' in data:
            return web.Response(text='El id del hidrante es necesario', status=http.HTTPStatus.NOT_ACCEPTABLE)
        
        if jwt_header:
            contador = HydrantController()
            return web.json_response(await contador.delete_hydrant(jwt_header, data['hydrant_id']), status=http.HTTPStatus.OK)
        else:
            return web.Response(text='No se proporcionó el encabezado "jwt"', status=http.HTTPStatus.UNAUTHORIZED)
