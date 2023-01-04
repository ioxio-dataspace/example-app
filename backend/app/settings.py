import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    # The base URL to the login portal
    OIDC_PROVIDER_URL: str = "https://login.sandbox.ioxio-dataspace.com"
    OIDC_SCOPES: str = "openid"
    OIDC_ACR_VALUES: str = "fake-auth"

    # The base URL to Product Gateway
    PRODUCT_GATEWAY_URL: str = "https://gateway.sandbox.ioxio-dataspace.com"

    # You can find values for OIDC_PROVIDER_URL and PRODUCT_GATEWAY_URL in the
    # dataspace configuration:
    # https://sandbox.ioxio-dataspace.com/.well-known/dataspace/dataspace-configuration.json
    # Find more information in the docs:
    # https://well-known-docs.sandbox.ioxio-dataspace.com/dataspace-configuration.html

    # The client ID and client secret for the app you created in the developer portal
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""

    # Secret used to protect the session
    # Currently this is generated during at script execution, so it's not a static value.
    # Don't do that in production
    SESSION_SECRET: str = secrets.token_urlsafe()

    # Timeout value for requests to OIDC provider
    OIDC_REQUEST_TIMEOUT: int = 30

    # Base URL of the application
    BASE_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


conf = Settings()
