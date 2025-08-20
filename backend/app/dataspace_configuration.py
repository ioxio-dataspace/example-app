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


async def get_product_gateway_url() -> str:
    dataspace_configuration = await get_dataspace_configuration()
    product_gateway_url = dataspace_configuration["product_gateway_url"]
    return product_gateway_url
