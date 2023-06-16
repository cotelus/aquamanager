import pytest
import re
from aiohttp.test_utils import TestClient, TestServer
from core.controllers.auth import AuthController
from aiohttp import web
from core.prepare_service import prepare_service
import aiohttp
from test.default.initRoutes import InitRoutes

class TestRouteAuth(InitRoutes):
    @pytest.mark.asyncio
    async def test_login_route(self):
        app = await prepare_service()
        self.setup()

        jwt_regex = r"^[\w-]*\.[\w-]*\.[\w-]*$"

        async with TestClient(TestServer(app)) as client:
            # Comprobar que funciona
            resp = await client.post('/login/', json={'username': 'admin', 'password': '1234'})
            assert resp.status == 202
            data = await resp.json()
            assert re.match(jwt_regex, data['token'])

            # Comprobar que no funciona
            resp = await client.post('/login/', json={'username': 'admin', 'password': 'no_pass'})
            assert resp.status == 401

        self.tear_down()
