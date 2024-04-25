from contextlib import asynccontextmanager
from logging import getLogger
from typing import Optional

import httpx
import jwt
from app.consents import router as consents_router
from app.dataspace_configuration import (
    get_dataspace_configuration,
    get_oidc_provider_url,
)
from app.settings import conf
from app.well_known import router as well_known_router
from authlib.common.urls import add_params_to_uri
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Cookie, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.routing import APIRouter
from httpx import Timeout
from pyjwt_key_fetcher import AsyncKeyFetcher
from starlette.middleware.sessions import SessionMiddleware

key_fetcher = AsyncKeyFetcher()
oauth = OAuth()
logger = getLogger(__name__)


async def register_oauth():
    oidc_provider_url = await get_oidc_provider_url()
    oauth.register(
        name="login_portal",
        client_id=conf.OIDC_CLIENT_ID,
        client_secret=conf.OIDC_CLIENT_SECRET,
        server_metadata_url=(oidc_provider_url + "/.well-known/openid-configuration"),
        client_kwargs={
            "scope": conf.OIDC_SCOPES,
            "timeout": Timeout(timeout=conf.OIDC_REQUEST_TIMEOUT),
        },
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await register_oauth()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=conf.SESSION_SECRET)
api_router = APIRouter()


@api_router.get("/settings")
async def get_settings():
    dataspace_configuration = await get_dataspace_configuration()
    dataspace_base_domain = dataspace_configuration["dataspace_base_domain"]
    return {
        "dataspaceBaseUrl": f"https://{dataspace_base_domain}",
        "consentPortalUrl": dataspace_configuration["consent_providers"][0]["base_url"],
        "definitionViewerUrl": dataspace_configuration["definition_viewer_url"],
        "dataspaceName": dataspace_configuration["dataspace_name"],
    }


@api_router.get("/login")
async def login(request: Request):
    """
    Start OpenID Connect login flow
    """
    return await oauth.login_portal.authorize_redirect(
        request=request,
        redirect_uri=f"{conf.BASE_URL}/api/auth",
        acr_values=conf.OIDC_ACR_VALUES,
    )


@api_router.get("/auth")
async def auth(request: Request):
    """
    Route used as return URL in OpenID Connect flow
    """
    try:
        token = await oauth.login_portal.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(status_code=401, detail=error.error)

    id_token = token["id_token"]
    access_token = token["access_token"]
    expires_in = token["expires_in"]

    response = RedirectResponse(url=conf.BASE_URL)

    if id_token:
        response.set_cookie(
            key="id_token",
            value=id_token,
            max_age=expires_in,
            httponly=True,
        )
    if access_token:
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=expires_in,
            httponly=True,
        )

    return response


@api_router.get("/logout")
async def logout(id_token: Optional[str] = Cookie(default=None)):
    """
    Start logout in OpenID Connect flow
    """
    metadata = await oauth.login_portal.load_server_metadata()
    end_session_endpoint = metadata["end_session_endpoint"]

    end_session_uri = add_params_to_uri(
        end_session_endpoint,
        (
            ("id_token_hint", id_token),
            ("post_logout_redirect_uri", conf.BASE_URL),
        ),
    )

    response = RedirectResponse(url=end_session_uri)

    response.delete_cookie(
        key="id_token",
        httponly=True,
    )
    response.delete_cookie(
        key="access_token",
        httponly=True,
    )
    return response


@api_router.get("/me")
async def user_profile(id_token: Optional[str] = Cookie(default=None)):
    """
    Return information about the currently authenticated user
    """
    if id_token:
        key_entry = await key_fetcher.get_key(id_token)
        try:
            token = jwt.decode(
                id_token,
                audience=conf.OIDC_CLIENT_ID,
                **key_entry,
            )
            return {
                "loggedIn": True,
                "email": token["email"],
            }
        except jwt.PyJWTError:
            logger.exception("Failed to decode JWT token")
            pass
    return {
        "loggedIn": False,
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
        dataspace_configuration = await get_dataspace_configuration()
        product_gateway_url = dataspace_configuration["product_gateway_url"]
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


api_router.include_router(consents_router)
app.include_router(api_router, prefix="/api")
app.include_router(well_known_router, prefix="/.well-known")


def main():
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)
