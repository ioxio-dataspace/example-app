import time
from typing import Optional

import httpx
import jwt
from app.dataspace_configuration import (
    get_consent_portal_url,
    get_oidc_provider_url,
    get_product_gateway_url,
)
from app.settings import conf
from app.utils import make_dsi
from async_lru import alru_cache
from fastapi import APIRouter, Cookie, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pyjwt_key_fetcher import AsyncKeyFetcher
from pyjwt_key_fetcher.errors import JWTKeyFetcherError

router = APIRouter()


class MissingConsent(Exception):
    pass


@alru_cache(maxsize=1)
async def get_key_fetcher() -> AsyncKeyFetcher:
    """
    Create and return a singleton instance of the AsyncKeyFetcher
    """
    oidc_provider_url = await get_oidc_provider_url()
    return AsyncKeyFetcher(valid_issuers=[oidc_provider_url])


async def parse_token(id_token: Optional[str]) -> str:
    """
    Parse id_token, validate it and return a subject (user id)
    :param id_token: ID Token from cookie
    :return: Sub (user ID)
    """
    if not id_token:
        raise HTTPException(401, "User not logged in")
    try:
        token = await validate_token(id_token=id_token)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(401, "User not logged in")

    return token["sub"]


async def validate_token(id_token: str) -> dict:
    """
    Validate an id_token
    raise: jwt.exceptions.InvalidTokenError If token is invalid
    """
    try:
        key_entry = await (await get_key_fetcher()).get_key(id_token)
    except JWTKeyFetcherError as e:
        raise jwt.exceptions.InvalidTokenError from e
    return jwt.decode(
        id_token,
        verify=True,
        audience=conf.OIDC_CLIENT_ID,
        issuer=await get_oidc_provider_url(),
        **key_entry,
    )


async def create_consent_request_token(sub) -> str:
    key = conf.PRIVATE_KEY
    oidc_provider_url = await get_oidc_provider_url()
    consent_portal_url = await get_consent_portal_url()

    now = int(time.time())
    crt = {
        "iss": f"https://{conf.PARTY_CONFIGURATION_DOMAIN}",
        "sub": sub,
        "subiss": oidc_provider_url,
        "acr": conf.OIDC_ACR_VALUES,
        "app": conf.OIDC_CLIENT_ID,
        "appiss": oidc_provider_url,
        "aud": consent_portal_url,
        "exp": now + conf.CONSENT_REQUEST_TOKEN_VALID_SECONDS,
        "iat": now,
    }
    headers = {
        "v": "0.2",
        "kid": conf.PRIVATE_KEY_ID or key.kid,
    }
    token = jwt.encode(
        payload=crt,
        key=key.private_key,
        algorithm=key.alg,
        headers=headers,
    )
    return token


async def fetch_consent_token(dsi: str, sub: str) -> Optional[str]:
    """
    Fetch Consent Token from Consent Portal
    :param dsi: Data Source Identifier
    :param sub: Subject for the consent
    :return: Consent Token if it has been granted already, None otherwise
    """
    consent_portal_url = await get_consent_portal_url()

    url = f"{consent_portal_url}/Consent/GetToken"
    cr_token = await create_consent_request_token(sub)
    headers = {"X-Consent-Request-Token": cr_token}
    payload = {"dataSource": dsi}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers, timeout=30)
    data = resp.json()
    if data.get("type") == "consentGranted":
        return data["consentToken"]
    else:
        raise MissingConsent


async def get_consent_verification_url(dsi: str, sub: str) -> Optional[str]:
    """
    Start consent flow. Request consent with a Consent Request Token,
    try to get a verification URL back from Consent Portal.
    :param dsi: Data Source Identifier
    :param sub: Subject of consent
    :return: URL to verify a consent in Consent Portal
    """
    consent_portal_url = await get_consent_portal_url()
    url = f"{consent_portal_url}/Consent/RequestConsents"
    cr_token = await create_consent_request_token(sub)
    headers = {"X-Consent-Request-Token": cr_token}
    payload = {"consentRequests": [{"dataSource": dsi, "required": True}]}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers, timeout=30)
    data = resp.json()
    if data.get("type") == "requestUserConsent":
        return data["requestUrl"]
    return None


@router.post("/data-product-consent/{data_product:path}")
async def fetch_data_product(
    data_product: str,
    request: Request,
    source=Query(),
    id_token: Optional[str] = Cookie(default=None),
):
    """
    A proxy from frontend to Product Gateway for data products that require consent.

    Before requesting the data it first obtains a consent token from Consent Portal.
    If it's the initial request, then the user must grant the consent
    in the Consent Portal UI.
    """
    # Validate ID Token to find a user ID that we use as a "sub" for consent request
    sub = await parse_token(id_token)

    dsi = make_dsi(conf.DATASPACE_BASE_DOMAIN, data_product, source)

    try:
        # Try to fetch a token from Consent Portal
        # IMPORTANT! Here we request consent token every time.
        # In real applications you might want to save the token in database
        # or a cookie and reuse it to avoid making extra API calls
        consent_token = await fetch_consent_token(dsi, sub)
    except MissingConsent:
        # if no token is returned then the user should approve the consent in UI
        verify_url = await get_consent_verification_url(dsi, sub)
        return JSONResponse(
            {
                "error": "Consent is required",
                "verifyUrl": verify_url,
            },
            status_code=403,
        )
    body = await request.json()
    headers = {
        "x-consent-token": consent_token,
        "authorization": f"Bearer {id_token}",
    }
    # Fetch data product
    async with httpx.AsyncClient() as client:
        product_gateway_url = await get_product_gateway_url()
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
