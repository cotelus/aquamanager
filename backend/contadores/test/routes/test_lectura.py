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
        await self.setup_test()

        async with TestClient(TestServer(app)) as client:
            # Comprobar que funciona
            resp = await client.get(
                '/lecturas/',
                headers={'Authorization': ADMIN_JWT}
            )
            try:
                assert resp.status == http.HTTPStatus.OK
                data = await resp.json()
                lecturas = data['result']
                assert len(lecturas) == 2
            finally:
                self.tear_down()
