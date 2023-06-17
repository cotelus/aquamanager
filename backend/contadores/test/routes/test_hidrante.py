import jwt
import pytest
import re
from aiohttp.test_utils import TestClient, TestServer
from core.prepare_service import prepare_service
from test.default.initRoutes import InitRoutes
import http
from test.default.initRoutes import ADMIN_JWT, NONADMIN_JWT, NORMALEMENTE_JWT


class TestRouteHidrante(InitRoutes):

    # Comprueba si se pueden obtener los hidrantes para un administrador
    @pytest.mark.asyncio
    async def test_hydrants_get_list_admin(self):
        app = await prepare_service()
        self.setup_test()

        hydrants_list = [
            {
                'counter': 123.2,
                'id': 1,
                'name': 'R17H3',
                'topic': '/hidrantes/r17h3',
                'user_id': 2,
                'valve_open': False
            },
            {
                'counter': 234.4,
                'id': 2,
                'name': 'R17H1',
                'topic': '/hidrantes/r17h1',
                'user_id': 2,
                'valve_open': True
            },
            {
                'counter': 1.0,
                'id': 3,
                'name': 'R02H1',
                'topic': '/hidrantes/r02h1',
                'user_id': 5,
                'valve_open': False
            }
        ]

        async with TestClient(TestServer(app)) as client:
            # Comprobar que funciona
            resp = await client.get(
                '/hidrantes/',
                headers={'jwt': ADMIN_JWT}
            )
            try:
                assert resp.status == http.HTTPStatus.OK
                data = await resp.json()
                hydrants = data['result']
                assert len(hydrants) == 3
                assert hydrants == hydrants_list
            finally:
                self.tear_down()

    # Comprueba si el login funciona
    @pytest.mark.asyncio
    async def test_hydrants_get_list_non_admin(self):
        app = await prepare_service()
        self.setup_test()

        hydrants_list = [
            {
                'counter': 123.2,
                'id': 1,
                'name': 'R17H3',
                'topic': '/hidrantes/r17h3',
                'user_id': 2,
                'valve_open': False
            },
            {
                'counter': 234.4,
                'id': 2,
                'name': 'R17H1',
                'topic': '/hidrantes/r17h1',
                'user_id': 2,
                'valve_open': True
            }
        ]

        async with TestClient(TestServer(app)) as client:
            # Comprobar que funciona
            resp = await client.get(
                '/hidrantes/',
                headers={'jwt': NONADMIN_JWT}
            )
            try:
                assert resp.status == http.HTTPStatus.OK
                data = await resp.json()
                hydrants = data['result']
                assert len(hydrants) == 2
                assert hydrants == hydrants_list
            finally:
                self.tear_down()
