from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api_router import api_router
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging, app_logger
from app.core.responses import success_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    app_logger.info("Starting SignalUp AI backend.")

    await connect_to_mongo()

    yield

    await close_mongo_connection()
    app_logger.info("SignalUp AI backend stopped.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SignalUp AI — IoT Device User Upgrade Propensity Prediction Backend",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return success_response(
        message="Welcome to SignalUp AI Backend.",
        data={
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "api_version": settings.API_V1_PREFIX,
        },
    )