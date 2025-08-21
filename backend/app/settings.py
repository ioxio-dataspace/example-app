from typing import Set

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # The dataspace base domain
    DATASPACE_BASE_DOMAIN: str = "sandbox.ioxio-dataspace.com"

    # Response headers from Product Gateway that gets forwarded in the response
    PRODUCT_GATEWAY_FORWARDED_HEADERS: Set[str] = {"x-powered-by", "server-timing"}

    # Access control keys for different DSIs
    ACCESS_CONTROL_KEYS: dict[str, str] = {}

    # Group to request API keys with, must match access control keys
    ACCESS_CONTROL_SUB: str = ""

    class Config:
        env_file = ".env"


conf = Settings()
