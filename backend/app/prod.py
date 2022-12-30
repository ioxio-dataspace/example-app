"""
You can ignore this file during local development.
This file is required to run the application inside a docker container.
"""

from fastapi.staticfiles import StaticFiles

from .main import app

app.mount("/", StaticFiles(directory="static", html=True), name="static")


def main():
    import uvicorn

    uvicorn.run("app.prod:app", host="0.0.0.0", port=8000)
