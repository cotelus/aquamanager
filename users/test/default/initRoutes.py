from pymongo import MongoClient
from core.controllers.auth import AuthController
from core.log.logger import logger
from core.load import get_venv

class InitRoutes():
    # Configura las propiedades iniciales para los tests individuales
    def setup(self):
        db = get_venv('AUTH_DB')

        if db is not None and type(db) is str:
            # Configura base de datos
            self.set_up_mongodb(db)

            # Inicia controladores
            auth = AuthController(db)
    
    def tear_down(self):
        db = get_venv('AUTH_DB')

        # Elimina la base de datos
        self.delete_mongo(db)

        # Elimina las instancias de los controladores
        AuthController.delete_instance()


    def set_up_mongodb(self, db_name):
        # Conectarse a la base de datos MongoDB con datos por defecto
        client = MongoClient(f'mongodb://{db_name}:27017/')
        db = client['db']

        # Verificar si la base de datos existe y crearla si no existe
        if 'db' not in client.list_database_names():
            db.create_collection("usuarios")

        # Verificar si la colección 'users' existe y crearla si no existe
        if "usuarios" not in db.list_collection_names():
            logger.debug("La colección 'usuarios' no existe. Creando nueva colección...")
            db.create_collection("usuarios")

        # Buscar el usuario 'admin' en la colección 'users'
        admin_user = db.usuarios.find_one({"username": "admin"})

        # Si el usuario 'admin' no existe, insertarlo en la colección 'users'
        if not admin_user:
            logger.debug("El usuario 'admin' no existe. Insertando usuario en la colección 'users'...")
            admin_data = {
                "username": "admin",
                "password": "1234",
                "admin": True
            }
            db.usuarios.insert_one(admin_data)

    def delete_mongo(self, database_name: str):
        # Conectarse a la base de datos MongoDB con datos por defecto
        client = MongoClient()
        db = client[database_name]

        # Eliminar todas las colecciones de la base de datos
        for collection_name in db.list_collection_names():
            db.drop_collection(collection_name)

        # Eliminar la base de datos
        client.drop_database(database_name)
