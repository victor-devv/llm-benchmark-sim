from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.benchmark_service.api.routers.base import router
from src.benchmark_service.config import config
from src.shared.utils.logger import logging as logger


def register_routers(app):
    app.include_router(router)


def start_application():
    app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routers(app)

    logger.info(
        f"🚀 {config.APP_NAME} running in {config.APP_ENV}. Listening on {config.PORT}"
    )
    return app


app = start_application()


@app.get("/", tags=["Health Check"])
def liveness_probe():
    return {"status": "success", "message": "App running!"}


@app.get("/healthz", tags=["Health Check"])
def read_root():
    return {"status": "success", "message": "App running!"}
