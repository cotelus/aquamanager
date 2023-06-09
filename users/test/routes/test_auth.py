import pytest
import re
from aiohttp.test_utils import TestClient, TestServer
from core.controllers.auth import AuthController
from aiohttp import web
from core.prepare_service import prepare_service
import aiohttp

# @pytest.mark.asyncio
# async def test_login():
#     auth = AuthController()
#     jwt_regex = r"^[\w-]*\.[\w-]*\.[\w-]*$"

#     # Comprobar que funciona
#     result = await auth.login('admin', 'admin_password')
#     assert re.match(jwt_regex, result)

#     # COmprobar que no funciona
#     try:
#         result = await auth.login('admin', 'not admin_password')
#     except Exception as e: 
#         assert e.body == web.HTTPUnauthorized().body

async def make_request(method, url, payload=None):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=payload) as response:
            return await response.json()

@pytest.mark.asyncio
async def test_login_route():
    app = await prepare_service()
    jwt_regex = r"^[\w-]*\.[\w-]*\.[\w-]*$"

    async with TestClient(TestServer(app)) as client:
        # Comprobar que funciona
        resp = await client.post('/login/', json={'username': 'admin', 'password': '1234'})
        assert resp.status == 202
        data = await resp.json()
        assert re.match(jwt_regex, data)

        # Comprobar que no funciona
        resp = await client.post('/login/', json={'username': 'admin', 'password': 'no_pass'})
        assert resp.status == 401
