# IOXIO Dataspace example app

This demo application is designed to show a practical example on how to create an
application using Dataspace technologies.

It consists of simple Python backend that is responsible for authentication and data
retrieval and React-based frontend application.

You can check the [online demo](https://example-app.demos.ioxio.dev) or run it locally
(check the [configuration](#configuration) section for the instructions).

Main idea is to demonstrate how to:

- Perform authentication in a dataspace
- Use the application credentials
- Retrieve data products from Product Gateway

## Repo structure

- [backend](./backend/) - FastAPI backend
  - [main.py](./backend/app/main.py) - All the backend routes, e.g for authentication or
    data retrieval
  - [settings.py](./backend/app/settings.py) - Backend configuration
- [frontend](./frontend) - React application
  - [containers](./frontend/src/containers) - Root containers for handling data products
  - [components](./frontend/src/components) - Stateless components to simplify following
    the containers' logic
  - [utils](./frontend/src/utils) - Some helpers, e.g for making network requests to
    backend

## Local installation

### Configuration

Before running the app locally, you have to:

1. Register an application in
   [Developer Portal](https://developer.sandbox.ioxio-dataspace.com/). Use the following
   values in the form:
   - Redirect URI: `http://localhost:3000/api/auth`
   - Logout redirect URI: `http://localhost:3000`
2. Obtain Client ID and Client secret of the application
3. Create [backend/.env](backend/.env) file based on
   [backend/.env.example](backend/.env.example) and set the variables with values taken
   from the previous step

### Pre-requisites

- [Python 3.9+](https://www.python.org/) - For running backend
- [Poetry](https://python-poetry.org/) - Python package manager
- [Node](https://nodejs.org/en/) - For running frontend
- [pnpm](https://pnpm.io/) - Node package manager
- (Optionally) [pre-commit](https://pre-commit.com/) - If you want to contribute to this
  repo, these hooks will be executed before a commit. Don't forget to run
  `pre-commit install` in this case after checking out the repo.

### Backend

```bash
cd backend
poetry install
# run it:
poetry run dev
```

### Frontend

```bash
cd frontend
pnpm install
# run it:
pnpm dev
```

Then open http://localhost:3000 in your browser.
