import jwt
import pytest
import re
from aiohttp.test_utils import TestClient, TestServer
from core.prepare_service import prepare_service
from test.default.initRoutes import InitRoutes
import http

class TestRouteHidrante(InitRoutes):

    # Comprueba si el login funciona
    @pytest.mark.asyncio
    async def test_hydrants_get_list(self):
        app = await prepare_service()
        self.setup_test()

        hydrants_list = [{'counter': 123.2,
             'id': 1,
             'topic': '/hidrantes/h1',
             'user_id': 2,
             'valve_open': False},
            {'counter': 234.4,
             'id': 2,
             'topic': '/hidrantes/h2',
             'user_id': 2,
             'valve_open': True},
            {'counter': 1.0,
             'id': 3,
             'topic': '/hidrantes/h3',
             'user_id': 5,
             'valve_open': False}]

        async with TestClient(TestServer(app)) as client:
            # Comprobar que funciona
            resp = await client.get('/hidrantes/')
            assert resp.status == http.HTTPStatus.OK
            data = await resp.json()
            hydrants = data['result']
            assert len(hydrants) == 3
            assert hydrants == hydrants_list


        self.tear_down()

    # Por si un test no se ejecuta bien, que elimine las bases de datos
    @pytest.fixture(scope='session')
    def pytest_sessionfinish(self, session, exitstatus):
        print("Ejecución de tests finalizada")
        self.tear_down()
