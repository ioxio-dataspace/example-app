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

ENV \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.2.2 \
    ZZZ_ENV_LAST_LINE=""

RUN : \
    # Install curl
    && apt-get update \
    && apt-get install -y curl \
    # Install and configure poetry
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true \
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
