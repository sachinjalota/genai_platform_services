from contextlib import asynccontextmanager  
from typing import AsyncGenerator, List  
from fastapi import FastAPI, Request  
from fastapi.exceptions import RequestValidationError, HTTPException  
from fastapi.middleware.cors import CORSMiddleware  
from starlette.responses import JSONResponse  
from src import unified_completion_router
from src.logging_config import Logger  
from src.config import (LOG_LEVEL, LOG_PATH, BASE_API_URL, BASE_API_KEY)  
from opik import OpikMiddleware  
import os  
  
# Lifespan for graceful startup and shutdown  
@asynccontextmanager  
async def lifespan(app: FastAPI) -> AsyncGenerator:  
    Logger.info("🚀 Application starting up...")  
    yield  
    Logger.info("🛑 Application shutting down...")  
  
def create_app(version: str = "0.1.0") -> FastAPI:  
    app = FastAPI(  
        title="Unified Completion API",  
        description="Unified Completion API supporting text and image via LiteLLM with OpenAI Specification",  
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
  
    # OPIK Middleware for observability integration  
    app.add_middleware(  
        OpikMiddleware,  
        service_name=os.getenv("OPIK_SERVICE_NAME", "litellm_service"),  
        log_level=os.getenv("OPIK_LOG_LEVEL", "INFO")  
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
        unified_completion_router.router,  
        prefix="/api/v1",  
        tags=["chat_completion"]  
    )  
  
    return app  
  
# Application Instance  
app = create_app()  