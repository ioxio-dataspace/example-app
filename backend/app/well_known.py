from typing import List

from app.settings import conf
from fastapi import APIRouter, Request, Response
from pydantic import AnyUrl, BaseModel

router = APIRouter()


class JWKSItem(BaseModel):
    kid: str
    kty: str
    use: str
    alg: str
    n: str
    e: str


class JWKSResponse(BaseModel):
    keys: List[JWKSItem]


class PartyConfiguration(BaseModel):
    jwks_uri: AnyUrl


def url_for(req: Request, name: str, **kwargs) -> str:
    """
    Get the URL for a route, absolute with our own BASE_URL
    """
    relative_url = req.scope["router"].url_path_for(name, **kwargs)
    return f"{str(conf.BASE_URL).rstrip('/')}{relative_url}"


@router.get(
    "/dataspace/party-configuration.json",
    summary="Party configuration",
    description="Party configuration",
    response_model=PartyConfiguration,
    tags=["configuration"],
)
async def party_configuration(req: Request, resp: Response):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return PartyConfiguration(
        jwks_uri=url_for(req, "jwks"),
    )


@router.get(
    "/jwks.json",
    name="jwks",
    summary="JWT Keys",
    description="Get public keys",
    response_model=JWKSResponse,
    tags=["configuration"],
)
async def jwks(resp: Response):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return {"keys": [conf.PRIVATE_KEY.jwk]}
