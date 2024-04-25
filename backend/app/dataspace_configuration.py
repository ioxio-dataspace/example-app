import httpx
from app.settings import conf
from async_lru import alru_cache
from fastapi import HTTPException


@alru_cache(ttl=30 * 60)
async def get_dataspace_configuration():
    """
    Fetch the dataspace configuration from the dataspace base domain
    """

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"https://{conf.DATASPACE_BASE_DOMAIN}/.well-known/dataspace/dataspace-configuration.json"
            )
        except httpx.HTTPError as exc:
            raise HTTPException(
                500, f"Error fetching dataspace configuration from {exc.request.url}"
            )
    return resp.json()


async def get_oidc_provider_url() -> str:
    dataspace_configuration = await get_dataspace_configuration()
    auth_providers = dataspace_configuration["authentication_providers"]
    oidc_provider_url = auth_providers["end_user"]["base_url"]
    return oidc_provider_url


async def get_consent_portal_url() -> str:
    dataspace_configuration = await get_dataspace_configuration()
    consent_portal_url = dataspace_configuration["consent_providers"][0]["base_url"]
    return consent_portal_url
