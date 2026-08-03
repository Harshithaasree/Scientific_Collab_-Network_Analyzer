from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from core import Base, Config, engine, get_config
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from granian import Granian
from granian.constants import Interfaces
from routes import router

Configuration: type[Config] = get_config()
config: Config = Configuration()
config.validate()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup: create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown: dispose engine
    await engine.dispose()


app = FastAPI(title="Research Management Platform", version="1.0.0", lifespan=lifespan)
app.include_router(router, prefix="/api")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, e: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "internal server error"})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    Granian(
        target="app.main:app",
        address="0.0.0.0",
        port=8000,
        interface=Interfaces.ASGI,
        reload=True,
    ).serve()
