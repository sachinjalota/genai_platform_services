import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.api.routers import chatcompletion_router
from src.logging_config import Logger
from src.config import (LOG_LEVEL, LOG_PATH, BASE_API_URL, BASE_API_KEY) 

# Lifespan for graceful startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    Logger.info("🚀 Application starting up...")
    yield
    Logger.info("🛑 Application shutting down...")

def create_app(version: str = "0.1.0") -> FastAPI:
    app = FastAPI(
        title="Chat Completion API",
        description="Chat Completion API supporting text and image via LiteLLM with OpenAI SDK",
        version=version,
        lifespan=lifespan,
    )

    # CORSMiddleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 

    # Custom middleware for CORS headers
    @app.middleware("http")
    async def add_cors_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

    # Exception Handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        Logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        Logger.error(f"HTTP error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    # Root Endpoint
    @app.get("/", tags=["Main"])
    async def read_root():
        return {"name": "Unified Completion API - Go to '/docs' for API documentation"}

    # Health Check Endpoint
    @app.get("/api/v1/health-check", tags=["Main"])
    async def health_check():
        return {"status": "ok"}

    # Include Routers
    app.include_router(
        chatcompletion_router.router,
        prefix="/api/v1",
        tags=["chatcompletion"]
    )

    return app

# Application Instance
app = create_app()