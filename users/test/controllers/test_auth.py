import pytest
import re
from core.controllers.auth import AuthController
from aiohttp import web

@pytest.mark.asyncio
async def test_login():
    auth = AuthController()
    jwt_regex = r"^[\w-]*\.[\w-]*\.[\w-]*$"

    # Comprobar que funciona
    result = await auth.login('admin', 'admin_password')
    assert re.match(jwt_regex, result)

    # COmprobar que no funciona
    try:
        result = await auth.login('admin', 'not admin_password')
    except Exception as e: 
        assert e.body == web.HTTPUnauthorized().body
