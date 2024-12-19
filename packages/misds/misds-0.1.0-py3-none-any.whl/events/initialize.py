from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.nacos.pynacos import ns


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    ns.register().send_heartbeat()

    yield

    ns.unregister()
