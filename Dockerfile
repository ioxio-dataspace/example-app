# ---- BUILD ENVIRONMENT ----- #

FROM digitallivinginternational/python-base:ubuntu22.04-python3.10-nginx-node as build

WORKDIR /src/frontend

ADD frontend ./
RUN pnpm install && pnpm build

# ---- RUNTIME ENVIRONMENT ----- #

FROM digitallivinginternational/python-base:ubuntu22.04-python3.10 as runtime

ENV LOGIN_RETURN_URL="/"

COPY --from=build /src/frontend/dist /src/app/static

WORKDIR /src/app
USER ${USER}

ADD backend ./
RUN poetry install

EXPOSE 8000
ENTRYPOINT ["poetry", "run", "serve"]
