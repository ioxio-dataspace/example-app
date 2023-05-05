import secrets

from app.keys import RsaPrivateKey
from pydantic import BaseSettings


class Settings(BaseSettings):
    # The base URL to the login portal.
    # You can find values for OIDC_PROVIDER_URL and PRODUCT_GATEWAY_URL in the
    # dataspace configuration:
    # https://sandbox.ioxio-dataspace.com/.well-known/dataspace/dataspace-configuration.json
    # Find more information in the docs:
    # https://well-known-docs.sandbox.ioxio-dataspace.com/dataspace-configuration.html
    OIDC_PROVIDER_URL: str = "https://login.sandbox.ioxio-dataspace.com"
    OIDC_SCOPES: str = "openid"
    OIDC_ACR_VALUES: str = "fake-auth"

    # The base URL to Product Gateway
    PRODUCT_GATEWAY_URL: str = "https://gateway.sandbox.ioxio-dataspace.com"

    # The base URL to Consent Portal
    CONSENT_PORTAL_URL: str = "https://consent.sandbox.ioxio-dataspace.com"
    # https:// + your party configuration domain
    CONSENT_REQUEST_TOKEN_ISSUER: str = "https://example-app.demos.ioxio.dev"
    # Validity time of consent request token
    CONSENT_REQUEST_TOKEN_VALID_SECONDS: int = 3600

    # The client ID and client secret for the app you created in the developer portal
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""

    # The dataspace domain you want to request consents for
    DATASPACE_DOMAIN: str = "sandbox.ioxio-dataspace.com"

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

    class Config:
        env_file = ".env"


conf = Settings()
