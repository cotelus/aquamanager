from aiohttp import web
from core.routes.contador import add_routes as contador_routes

async def prepare_service():
    #TODO  Inicializar controladores


    # Se crea la aplicación
    app = web.Application()

    # Se inicializa la tabla de rutas
    routes = web.RouteTableDef()
    
    # Se añaden las rutas del contador
    contador_routes(routes)

    # Se añade la tabla de rutas a la aplicación
    app.add_routes(routes)

    # Se devuelve la aplicación
    return app
