import httpx
from app.settings import conf
from fastapi import HTTPException

DATASPACE_CONFIGURATION = None


async def get_dataspace_configuration():
    """
    Fetch the dataspace configuration from the dataspace base domain
    """
    global DATASPACE_CONFIGURATION
    if DATASPACE_CONFIGURATION:
        return DATASPACE_CONFIGURATION

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"https://{conf.DATASPACE_BASE_DOMAIN}/.well-known/dataspace/dataspace-configuration.json"
            )
        except httpx.HTTPError as exc:
            raise HTTPException(
                500, f"Error fetching dataspace configuration from {exc.request.url}"
            )
    DATASPACE_CONFIGURATION = resp.json()
    return DATASPACE_CONFIGURATION
