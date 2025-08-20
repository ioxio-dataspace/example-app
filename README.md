# IOXIO Dataspace example app

This demo application is designed to show a practical example on how to create an
application that connects to a Dataspace built with the IOXIO Dataspace technology.

It consists of a simple Python [FastAPI](https://fastapi.tiangolo.com) backend that is
responsible for data retrieval and a React-based frontend application.

You can try the [online demo](https://example-app.demos.ioxio.dev) or check the
[configuration](#configuration) section for instructions on how to run this code
locally.

Main idea is to demonstrate how to:

- Retrieve data products from Product Gateway
- Retrieve data from data sources that are using Dataspace managed API tokens

## Repo structure

- [backend](./backend/) - Python [FastAPI](https://fastapi.tiangolo.com/) backend
  - [main.py](./backend/app/main.py) - All the backend routes, e.g. for data retrieval
  - [access_control.py](./backend/app/consents.py) - Logic for getting API tokens for
    sources using Dataspace managed API tokens
  - [settings.py](./backend/app/settings.py) - Backend configuration
- [frontend](./frontend) - React application
  - [containers](./frontend/src/containers) - Root containers for handling data products
  - [components](./frontend/src/components) - Stateless components to simplify following
    the containers' logic
  - [utils](./frontend/src/utils) - Some helpers, e.g. for making network requests to
    the backend

## Local installation

### Configuration

No configuration is necessary to get started with testing the app locally. However, if
you want to also test data retrieval from a data source that requires dataspace managed
API tokens, you need to:

1. Create a group in the
   [Sandbox Developer Portal](https://developer.sandbox.ioxio-dataspace.com/).
2. Request that your group gets access to the data source.
3. Create the [backend/.env](backend/.env) file based on
   [backend/.env.example](backend/.env.example).
4. Get your access control keys from the
   [Sandbox Developer Portal](https://developer.sandbox.ioxio-dataspace.com/) and
   configure `ACCESS_CONTROL_KEYS` like:
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
