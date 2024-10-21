import httpx
from app.dataspace_configuration import get_product_gateway_url
from app.settings import conf
from async_lru import alru_cache


# API tokens are by default valid for 1 hour, this caches them for 59 minutes
@alru_cache(ttl=59 * 60)
async def get_api_token(dsi: str) -> str:
    """
    Simple example of how to get an API token. Assumes one access control key is used per DSI, and all access control
    keys are for one "sub" - as they should be.
    """
    access_control_key = conf.ACCESS_CONTROL_KEYS[dsi]
    body = {
        "aud": dsi,
        "sub": conf.ACCESS_CONTROL_SUB,
        "accessControlKey": access_control_key,
    }

    async with httpx.AsyncClient() as client:
        product_gateway_url = await get_product_gateway_url()
        result = await client.post(
            f"{product_gateway_url}/api/v1/api-token/request",
            json=body,
            timeout=30,
        )
        result.raise_for_status()

        response = result.json()
        return response["apiToken"]
