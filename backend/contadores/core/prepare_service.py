from aiohttp import web
from core.routes.hidrante import add_routes as hydrant_routes
from core.load import get_venv
from core.controllers.hidrante import HydrantController

async def prepare_service():
    # Se crea la aplicación
    app = web.Application()

    counter_db = get_venv("CONTADORES_DB") or "contadores-db"

    # Se inicializan los controladores
    hidrante = HydrantController(
        db_name = counter_db
    )

    # Se inicializa la tabla de rutas
    routes = web.RouteTableDef()
    
    # Se añaden las rutas del contador
    hydrant_routes(routes)

    # Se añade la tabla de rutas a la aplicación
    app.add_routes(routes)

    # Se devuelve la aplicación
    return app
