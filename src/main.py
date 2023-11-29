import logging
import os
from typing import Any

from fastapi import FastAPI, status
from mangum import Mangum
from pydantic import BaseModel

from src.api.v1 import v1_router
from src.core.config import settings
from src.core.log_filters import EndpointFilter

# from src.core.logger.api_logger import ApiLogger
# from src.core.logger.logging_context_route import LoggingContextRoute
from src.exceptions.error_handle_middleware import ErrorHandlingMiddleware
from src.core.logger.loguru_route_logging import LoguruRouteLogging
from src.schemas.dummy import DummyResponse

# from fastapi.middleware.cors import CORSMiddleware

# "Receive Event" Annotation
EventAny = Any

# 環境によって設定制御
env = os.getenv("ENV")
if env is None:
    app = FastAPI(
        title=settings.title,
        version=settings.version,
        # description=settings.description,
        # docs_url=settings.docs_url,
        # openapi_prefix=settings.openapi_prefix,
        # openapi_url=settings.openapi_url,
    )
else:
    app = FastAPI(
        root_path="/dev",
        title=settings.title,
        version=settings.version,
        # description=settings.description,
        # docs_url=settings.docs_url,
    )
# app.router.route_class = RouteLogging
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoguruRouteLogging)

app.include_router(v1_router, prefix="/v1")

# origins = [
#     "http://excample.com",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 除外したいエンドポイントを指定
excluded_endpoints = ["/favicon.ico"]
# フィルター追加
logging.getLogger("uvicorn.access").addFilter(EndpointFilter(excluded_endpoints))


@app.get(
    "/dummy",
    summary="Test Path After UpdatingDocker Image",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=DummyResponse,
)
def dummy() -> DummyResponse:
    """
    Call this path.

    If you push new Docker Image to ECR use "deploy.sh"
    """
    return DummyResponse(status="dummy")


class HealthCheck(BaseModel):

    """Response model to validate and return when performing a health check."""

    status: str = "OK"


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """Calculate speed as distance divided by time.


    Returns:
        ABC
    """
    return HealthCheck(status="OK")


def handler(event: EventAny, context: EventAny):
    # ApiLogger.info(event)

    asgi_handler = Mangum(app)
    return asgi_handler(event, context)
