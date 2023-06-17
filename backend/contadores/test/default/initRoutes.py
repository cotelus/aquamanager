from pymongo import MongoClient
from core.controllers.lectura import LecturaController
from core.controllers.hidrante import HydrantController
from core.log.logger import logger
from core.load import get_venv

ADMIN_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiYWRtaW4iOnRydWV9.PSvNGtW-zZMibWQKYldIgrpEc_uJEPKZeR1ErtZd17s"
NONADMIN_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im5vbmFkbWluIiwidXNlcl9pZCI6MiwiYWRtaW4iOmZhbHNlfQ.xq4fGUVdPt-WJ-OZiKa-GqP1JEVS1T_Bthw_Y1kDnnc"
NORMALEMENTE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im5vcm1hbGVtZW50ZSIsInVzZXJfaWQiOjMsImFkbWluIjpmYWxzZX0.eJlyzr5nOjl4Y4nj16sf7wJUR2vJqibFrhx7Rk-Di0E"

class InitRoutes():
    # Configura las propiedades iniciales para los tests individuales
    def setup_test(self):
        db = get_venv('CONTADORES_DB')

        if db is not None and type(db) is str:
            # Configura base de datos
            self.set_up_mongodb(db)

    def tear_down(self):
        db = get_venv('CONTADORES_DB')

        # Elimina la base de datos
        self.delete_mongo(db)

        # Elimina las instancias de los controladores
        LecturaController.delete_instance()
        HydrantController.delete_instance()

    def set_up_mongodb(self, db_name):
        # Conectarse a la base de datos MongoDB con datos por defecto
        client = MongoClient(f'mongodb://{db_name}:27017/')
        db = client['db']

        # Verificar si la base de datos existe y crearla si no existe
        if 'db' not in client.list_database_names():
            db.create_collection("lecturas")
            db.create_collection("hidrantes")

        # Verificar si la colección 'hidrantes' existe y crearla si no existe
        if "hidrantes" not in db.list_collection_names():
            logger.debug(
                "La colección 'hidrantes' no existe. Creando nueva colección...")
            db.create_collection("hidrantes")

         # Verificar si la colección 'users' existe y crearla si no existe
        if "lecturas" not in db.list_collection_names():
            logger.debug(
                "La colección 'lecturas' no existe. Creando nueva colección...")
            db.create_collection("lecturas")

        # Si el usuario 'admin' no existe, insertarlo en la colección 'users'
        hydrant_data = [
            {
                "id": 1,
                "name": "R17H3",
                "valve_open": False,
                "counter": 123.2,
                "topic": "/hidrantes/r17h3",
                "user_id": 2
            },
            {
                "id": 2,
                "name": "R17H1",
                "valve_open": True,
                "counter": 234.4,
                "topic": "/hidrantes/r17h1",
                "user_id": 2
            },
            {
                "id": 3,
                "name": "R02H1",
                "valve_open": False,
                "counter": 1,
                "topic": "/hidrantes/r02h1",
                "user_id": 5
            }
        ]
        db.hidrantes.insert_many(hydrant_data)

    def delete_mongo(self, db_name: str):
        # Conectarse a la base de datos MongoDB con datos por defecto
        client = MongoClient(f'mongodb://{db_name}:27017/')
        db = client['db']

        # Eliminar todas las colecciones de la base de datos
        for collection_name in db.list_collection_names():
            db.drop_collection(collection_name)

        # Eliminar la base de datos
        client.drop_database('db')
