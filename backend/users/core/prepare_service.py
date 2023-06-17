from aiohttp import web
from core.routes.auth import add_routes as user_routes
from core.controllers.auth import AuthController
from core.load import get_venv

async def prepare_service():
    # Se crea la aplicación
    app = web.Application()

    # Se obtienen variables de entorno
    auth_db = get_venv("AUTH_DB") or "user-db"

    # Se inicializan los controladores
    auth = AuthController(
        db_name = auth_db
    )

    # Se inicializa la tabla de rutas
    routes = web.RouteTableDef()
    
    # Se añaden las rutas del contador
    user_routes(routes)

    # Se añade la tabla de rutas a la aplicación
    app.add_routes(routes)

    # Se devuelve la aplicación
    return app
