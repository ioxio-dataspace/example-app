import secrets
from typing import Optional, Set

from app.keys import RsaPrivateKey
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # The dataspace base domain
    DATASPACE_BASE_DOMAIN: str = "sandbox.ioxio-dataspace.com"

    # The client ID and client secret for the app you created in the developer portal
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""
    OIDC_SCOPES: str = "openid"
    OIDC_ACR_VALUES: str = "fake-auth"

    # Response headers from Product Gateway that gets forwarded in the response
    PRODUCT_GATEWAY_FORWARDED_HEADERS: Set[str] = {"x-powered-by", "server-timing"}

    # Your party configuration domain
    PARTY_CONFIGURATION_DOMAIN: str = "example-app.demos.ioxio.dev"
    # Validity time of consent request token
    CONSENT_REQUEST_TOKEN_VALID_SECONDS: int = 3600

    # Secret used to protect the session
    # By default this generates a new secret on each startup. In an actual deployment
    # you should provide it as an environment variable or through the .env file
    SESSION_SECRET: str = secrets.token_urlsafe()

    # Timeout value for requests to OIDC provider
    OIDC_REQUEST_TIMEOUT: int = 30

    # Base URL of the application
    BASE_URL: str = "http://localhost:3000"

    # Key used for signing consent request tokens
    # NOTE! Since this is a demo application, we set this value publicly.
    # For real applications, it should not be exposed.
    PRIVATE_KEY: RsaPrivateKey = """
    -----BEGIN RSA PRIVATE KEY-----
    MIICXgIBAAKBgQDSvCZaKS1omIe7IeJCXToxzOowsxsueFtgEUx4fLJM78d5T/2P
    G1D0FUik0qbXpRqopYvUNBZ7wPZXIZcvtHE4FYfrPFgYHgIBFyoEmbI2g91PkcYm
    I7aap6aJb2KppNLch9Sc4VzWHuN4WVSYSGqLLg06Ur1N7C7+NL/7k7EmGQIDAQAB
    AoGBAIdVnau5VhgeHMzo7c2A4aap2px76bDmSohfk6StMDSIqKoX3NbSzCJ0qLpx
    LgS/W2eDKVGWQfon6gv63oUcdLhNbkD0eAqXUR/jY9MMawmgrrQl7J3kc4Io/Yn0
    M5IalnFuK7ZLNzMV01Lsw5ZyZLhLc7lAIskEw+6QGssvZlQBAkEA7kRSvTBGBRAO
    Ap3oonL33ELZkfhm1mzRqIMeSZJv1MQvxfapB76pVyUPfrqmzxCATFUTzJzG3zpo
    XbO46pfskQJBAOJrQ2wsD1DIvUiXQwnMUmNU2QrxMnk4OjNzGwr32GgdyJyDd27f
    iRs0jSdY3YklnpBJa6VwhHlv3o/mF0qLBQkCQQCUaMA0kT37500iuiLuFLhoXMdS
    UawUgYFx+gHCh9DacTzkjMgqR8sIuc/V+wLt1PRlF1UWzMxevO3G96wFi43RAkBo
    n13hPx64mnl0cIjGn0Y2pf9AoiFLiCLEoVyOneW+fnyzbcAjWGFXU9oho1uCwwJY
    88QtByf/oSS7Y3vBsylZAkEAhiJHtn5ZAii0LhWSz/55vYlWVTnvUwRppm4nIEgw
    VIvg/B38+PGLctRTszT9lyg/XDUPXCufqsXPMeaWL3h/7A==
    -----END RSA PRIVATE KEY-----
    """

    # kid
    PRIVATE_KEY_ID: Optional[str] = None

    # Access control keys for different DSIs
    ACCESS_CONTROL_KEYS: dict[str, str] = {}

    # Group to request API keys with, must match access control keys
    ACCESS_CONTROL_SUB: str = ""

    class Config:
        env_file = ".env"


conf = Settings()
