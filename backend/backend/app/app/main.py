from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
# import sentry_sdk
from osintbuddy import discover_plugins
from app.api.api_v1.api import api_router
from app.core.config import settings


# if settings.SENTRY_DSN:
#    # @todo find alternative to sentry...
#     https://github.com/getsentry/sentry-python/issues/1950#issuecomment-1526099852
#     sentry_sdk.init(
#         dsn="https://c5f217ca357c468cbb7cfe663318018f@o567628.ingest.sentry.io/4505363615711232",
#         traces_sample_rate=1.0,  # capture 100%
#     )

def redis_cache():
    return caches.get(CACHE_KEY)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    default_response_class=UJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "User-Agent",
        "If-Modified-Since",
        "Cache-Control",
        "Authorization",
        "Access-Control-Allow-Origin"
    ],
    expose_headers=[
        "x-osintbuddy-user",
        "x-osintbuddy-error"
    ],
)


def app_openapi_schema(app):
    """Return openapi_schema. cached."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.API_V1_STR,
        description=settings.PROJECT_DESCRIPTION,
        routes=app.routes,
    )
    # @todo upload a .png
    openapi_schema["info"]["x-logo"] = {
        "url": "https://raw.githubusercontent.com/jerlendds/osintbuddy/main/docs/assets/logo-watermark.svg"
    }
    return openapi_schema


app.include_router(api_router, prefix=settings.API_V1_STR)
app.openapi_schema = app_openapi_schema(app)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()
    import sys
    sys.exit()


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend(settings.REDIS_URL)
    caches.set(CACHE_KEY, rc)



# @app.get("/sentry-debug")
# async def trigger_error():
#     division_by_zero = 1 / 0
#     return division_by_zero
