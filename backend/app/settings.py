import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    # The base URL to the login portal
    OIDC_PROVIDER: str = "https://login.sandbox.ioxio-dataspace.com"
    OIDC_SCOPES: str = "openid"
    OIDC_ACR_VALUES: str = "fake-auth"

    # The client ID and client secret for the app you created in the developer portal
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""

    # Secret used to protect the session
    SESSION_SECRET: str = secrets.token_urlsafe()

    # Timeout value for requests to OIDC provider
    OIDC_REQUEST_TIMEOUT: int = 30

    # The base URL to Product Gateway
    PRODUCT_GATEWAY_URL: str = "https://gateway.sandbox.ioxio-dataspace.com"

    # Page that user should be redirected to after logging in
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


conf = Settings()
