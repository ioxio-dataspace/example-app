# ---- BUILD ENVIRONMENT ----- #

FROM node:18.12-slim as build

WORKDIR /src/frontend

ADD frontend ./
RUN : \
    && npm install -g pnpm \
    && pnpm install \
    && pnpm build \
    && :

# ---- RUNTIME ENVIRONMENT ----- #

FROM python:3.10-slim as runtime

# TODO: change it to real URL after deployment
ENV \
    BASE_URL="http://localhost:3000" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.2.2 \
    POETRY_VENV_PATH="/.venv" \
    ZZZ_ENV_LAST_LINE=""

RUN : \
    # Install curl
    && apt-get update \
    && apt-get install -y curl \
    # Install poetry
    && curl -sSL https://install.python-poetry.org | python3 - \
    # Configure poetry
    && mkdir "${POETRY_VENV_PATH}" \
    && poetry config virtualenvs.in-project false \
    && poetry config virtualenvs.path "${POETRY_VENV_PATH}" \
    # Cleanup
    && apt-get remove -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && :

# Copy static frontend from the build target
COPY --from=build /src/frontend/dist /src/app/static

WORKDIR /src/app

# Add backend code and install python dependencies
ADD backend ./
RUN poetry install

EXPOSE 8080
ENTRYPOINT ["poetry", "run", "serve"]
