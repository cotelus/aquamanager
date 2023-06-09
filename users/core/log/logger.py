import logging

# Se configura el sistema de logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('contadores')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('contadores_service.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
