from logging import getLogger
from typing import Optional

import httpx
from app.access_control import get_api_token
from app.dataspace_configuration import (
    get_dataspace_configuration,
    get_product_gateway_url,
)
from app.settings import conf
from app.utils import make_dsi
from fastapi import Cookie, FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

logger = getLogger(__name__)


app = FastAPI()
api_router = APIRouter()


@api_router.get("/settings")
async def get_settings():
    dataspace_configuration = await get_dataspace_configuration()
    dataspace_base_domain = dataspace_configuration["dataspace_base_domain"]
    return {
        "dataspaceBaseUrl": f"https://{dataspace_base_domain}",
        "definitionViewerUrl": dataspace_configuration["definition_viewer_url"],
        "dataspaceName": dataspace_configuration["dataspace_name"],
    }


@api_router.post("/data-product/{data_product:path}")
async def fetch_data_product(
    data_product: str,
    request: Request,
    source=Query(),
    id_token: Optional[str] = Cookie(default=None),
):
    """
    Simple proxy from frontend to Product Gateway.

    Some requests to the Product Gateway require authentication of
    the application, thus we route all the request through the backend.
    """

    body = await request.json()
    headers = {}
    if id_token:
        headers["authorization"] = f"Bearer {id_token}"

    async with httpx.AsyncClient() as client:
        product_gateway_url = await get_product_gateway_url()

        # If we have an access control key configured for the source, get an API token for the request
        dsi = make_dsi(conf.DATASPACE_BASE_DOMAIN, data_product, source)
        if dsi in conf.ACCESS_CONTROL_KEYS:
            headers["X-API-Key"] = await get_api_token(dsi)

        resp = await client.post(
            f"{product_gateway_url}/{data_product}",
            params={"source": source},
            json=body,
            headers=headers,
            timeout=30,
        )
        forwarded_headers = {
            header: value
            for header, value in resp.headers.items()
            if header in conf.PRODUCT_GATEWAY_FORWARDED_HEADERS
        }
    return JSONResponse(resp.json(), resp.status_code, headers=forwarded_headers)


app.include_router(api_router, prefix="/api")


def main():
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)
