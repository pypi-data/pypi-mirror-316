import logging

import jsonschema_rs
import structlog
from langgraph.errors import EmptyInputError, InvalidUpdateError
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import langgraph_api.config as config
import langgraph_api.patch  # noqa: F401
from langgraph_api.api import routes
from langgraph_api.errors import (
    overloaded_error_handler,
    validation_error_handler,
    value_error_handler,
)
from langgraph_api.http_logger import AccessLoggerMiddleware
from langgraph_api.lifespan import lifespan
from langgraph_license.middleware import LicenseValidationMiddleware
from langgraph_storage.retry import OVERLOADED_EXCEPTIONS

logging.captureWarnings(True)
logger = structlog.stdlib.get_logger(__name__)

app = Starlette(
    routes=routes,
    lifespan=lifespan,
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=config.CORS_ALLOW_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(LicenseValidationMiddleware),
        Middleware(AccessLoggerMiddleware, logger=logger),
    ],
    exception_handlers={
        ValueError: value_error_handler,
        InvalidUpdateError: value_error_handler,
        EmptyInputError: value_error_handler,
        jsonschema_rs.ValidationError: validation_error_handler,
    }
    | {exc: overloaded_error_handler for exc in OVERLOADED_EXCEPTIONS},
)
