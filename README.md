# IOXIO Dataspace example app

This demo application is designed to show a practical example on how to create an
application that connects to a Dataspace built with the IOXIO Dataspace technology.

It consists of a simple Python [FastAPI](https://fastapi.tiangolo.com) backend that is
responsible for authentication and data retrieval and React-based frontend application.

You can try the [online demo](https://example-app.demos.ioxio.dev) or check the
[configuration](#configuration) section for instructions on how to run this code
locally.

Main idea is to demonstrate how to:

- Retrieve data products from Product Gateway
- Perform authentication in a dataspace
- Use the authentication tokens for data products
- Request data products that require consent

## Repo structure

- [backend](./backend/) - Python [FastAPI](https://fastapi.tiangolo.com/) backend
  - [main.py](./backend/app/main.py) - All the backend routes, e.g. for authentication
    or data retrieval
  - [access_control.py](./backend/app/consents.py) - Logic for getting API tokens for
    sources using Dataspace managed API tokens
  - [consents.py](./backend/app/consents.py) - Code related to requesting data products
    that require a consent
  - [well_known.py](./backend/app/well_known.py) - Party configuration related endpoints
  - [settings.py](./backend/app/settings.py) - Backend configuration
- [frontend](./frontend) - React application
  - [containers](./frontend/src/containers) - Root containers for handling data products
  - [components](./frontend/src/components) - Stateless components to simplify following
    the containers' logic
  - [utils](./frontend/src/utils) - Some helpers, e.g. for making network requests to
    the backend

## Local installation

### Configuration

Before running the app locally, you have to:

1. Create a group in [Developer Portal](https://developer.sandbox.ioxio-dataspace.com/).
   and set party configuration domain to `example-app.demos.ioxio.dev`. Or follow the
   [guide](https://docs.ioxio.dev/guides/managing-groups/#creating-and-hosting-party-configuration)
   to create and host your own.
2. Register new application in the
   [Developer Portal](https://developer.sandbox.ioxio-dataspace.com/). Use the following
   values in the form:

   - Redirect URI: `http://localhost:3000/api/auth`
   - Logout redirect URI: `http://localhost:3000`

   Note: In the next step you will need the Client ID and Client secret that get
   generated when you complete the registration of the application.

3. Create the [backend/.env](backend/.env) file based on
   [backend/.env.example](backend/.env.example) and set `OIDC_CLIENT_ID` and
   `OIDC_CLIENT_SECRET` variables with the values from the previous step.
4. Additionally, if you host your own party configuration, then set the corresponding
   key as `PRIVATE_KEY`, set `PRIVATE_KEY_ID` and update `PARTY_CONFIGURATION_DOMAIN`.
5. If you want to test access control keys, get your access control keys from the
   [Developer Portal](https://developer.sandbox.ioxio-dataspace.com/) and configure
   `ACCESS_CONTROL_KEYS` like:
   ```
   ACCESS_CONTROL_KEYS={"dpp://.../": "ABC123..."}
   ```
   Multiple keys can be set for separate DSIs by separating the pairs with commas. You
   will also have to set `ACCESS_CONTROL_SUB` to the group your application uses to
   access the source.

### Pre-requisites

- [Python 3.11 - 3.13](https://www.python.org/) - For running the backend
- [Poetry 1.8.2+](https://python-poetry.org/) - Python dependency management tool
- [Node 18+](https://nodejs.org/en/) - For running the frontend
- [pnpm 8.15+](https://pnpm.io/) - Node package manager
- [pre-commit](https://pre-commit.com/) - Runs hooks before you commit to e.g. format
  your code. Make sure you run `pre-commit install` after checking out the repo.

### Backend

```bash
cd backend
poetry install

poetry run dev
```

### Frontend

```bash
cd frontend
pnpm install

pnpm dev
```

Then open http://localhost:3000 in your browser.
