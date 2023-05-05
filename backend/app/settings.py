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

    # Key used for signing consent request tokens
    PRIVATE_KEY: RsaPrivateKey

    # The client ID and client secret for the app you created in the developer portal
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""

    # The domain you want to requests consents for
    DATASPACE_DOMAIN: str = "sandbox.ioxio-dataspace.com"

    # Secret used to protect the session
    # By default this generates a new secret on each startup. In an actual deployment
    # you should provide it as an environment variable or through the .env file
    SESSION_SECRET: str = secrets.token_urlsafe()

    # Timeout value for requests to OIDC provider
    OIDC_REQUEST_TIMEOUT: int = 30

    # Base URL of the application
    BASE_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


conf = Settings()
