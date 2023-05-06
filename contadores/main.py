from aiohttp import web
import argparse

from core.prepare_service import prepare_service

parser = argparse.ArgumentParser(description='servicio-contador')
parser.add_argument('--path')
parser.add_argument('--port')

if __name__ == '__main__':
    args = parser.parse_args()

    # Se prepara el servicio
    app = prepare_service()

    # Se lanza el servicio
    web.run_app(
        app,
        path=args.path,
        port=args.port
    )
