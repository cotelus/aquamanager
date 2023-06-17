import jwt
import pytest
import re
from aiohttp.test_utils import TestClient, TestServer
from core.controllers.auth import AuthController
from aiohttp import web
from core.prepare_service import prepare_service
import aiohttp
from test.default.initRoutes import InitRoutes
from core.controllers.auth import SECRET_KEY
import http

class TestRouteAuth(InitRoutes):

    # Comprueba si el login funciona
    @pytest.mark.asyncio
    async def test_login_route(self):
        app = await prepare_service()
        self.setup_test()

        jwt_regex = r"^[\w-]*\.[\w-]*\.[\w-]*$"

        async with TestClient(TestServer(app)) as client:
            # Comprobar que funciona
            resp = await client.post('/login/', json={'username': 'admin', 'password': '1234'})
            assert resp.status == http.HTTPStatus.ACCEPTED
            data = await resp.json()
            assert re.match(jwt_regex, data['token'])

            # Comprobar que no funciona
            resp = await client.post('/login/', json={'username': 'admin', 'password': 'no_pass'})
            assert resp.status == http.HTTPStatus.UNAUTHORIZED

        self.tear_down()

    # Comprueba si el jwt de un login válido tiene el formato adecuado
    @pytest.mark.asyncio
    async def test_login_jwt(self):
        app = await prepare_service()
        self.setup_test()

        jwt_regex = r"^[\w-]*\.[\w-]*\.[\w-]*$"

        async with TestClient(TestServer(app)) as client:
            # Comprobar que funciona
            resp = await client.post('/login/', json={'username': 'admin', 'password': '1234'})
            assert resp.status == http.HTTPStatus.ACCEPTED
            data = await resp.json()
            decoded_token = jwt.decode(data['token'], SECRET_KEY, algorithms=['HS256'])
            assert re.match(jwt_regex, data['token'])
            assert decoded_token['admin'] == True
            assert decoded_token['user_id'] == 1
            assert decoded_token['hydrants'] == [1, 2, 3, 4, 5, 6, 7]
            assert decoded_token['username'] == 'admin'

        self.tear_down()

    # Una vez generato el token jwt, pide desencriptarlo
    @pytest.mark.asyncio
    async def test_decrypt_jwt(self):
        app = await prepare_service()
        self.setup_test()

        jwt_regex = r"^[\w-]*\.[\w-]*\.[\w-]*$"

        async with TestClient(TestServer(app)) as client:
            # Comprobar que funciona
            resp = await client.post('/login/', json={'username': 'admin', 'password': '1234'})
            assert resp.status == http.HTTPStatus.ACCEPTED
            data = await resp.json()
            decoded_token = jwt.decode(data['token'], SECRET_KEY, algorithms=['HS256'])

            # Comprobar que no funciona
            resp = await client.get('/decryptjwt/', json={'jwt': data['token']})
            assert resp.status == http.HTTPStatus.OK
            data = await resp.json()
            assert data == decoded_token

        self.tear_down()

    # Por si un test no se ejecuta bien, que elimine las bases de datos
    @pytest.fixture(scope='session')
    def pytest_sessionfinish(self, session, exitstatus):
        print("Ejecución de tests finalizada")
        self.tear_down()
