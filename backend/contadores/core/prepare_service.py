from aiohttp import web
from core.routes.hidrante import add_routes as hydrant_routes
from core.routes.lectura import add_routes as reading_routes
from core.load import get_venv
from core.controllers.hidrante import HydrantController
from core.controllers.lectura import LecturaController

async def prepare_service():
    # Se crea la aplicación
    app = web.Application()

    counter_db = get_venv("CONTADORES_DB") or "contadores-db"
    reading_db = get_venv("LECTURAS_DB") or "lecturas-influxdb"

    # Se inicializan los controladores
    hidrante = HydrantController(
        db_name = counter_db
    )

    lectura = LecturaController(
        db_name = reading_db
    )

    # Se inicializa la tabla de rutas
    routes = web.RouteTableDef()
    
    # Se añaden las rutas
    hydrant_routes(routes)
    reading_routes(routes)

    # Se añade la tabla de rutas a la aplicación
    app.add_routes(routes)

    # Se devuelve la aplicación
    return app
