from contextlib import asynccontextmanager
from typing import Callable
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from integra_bridge.common.settings import SETTINGS
from integra_bridge.patterns.singleton import SingletonMeta
from integra_bridge.routers.v1.base import base_router
from integra_bridge.common.dependency_manager import dm


class Bridge(metaclass=SingletonMeta):
    def __init__(
            self,
            title: str = "Python-bridge",
            address: str = '',
            description: str = "Библиотека предназначена для подключения внешних Python сервисов",
            manual_path: Path | None = Path('')
    ):
        self.__title = title
        self.__address = address
        self.__description = description
        self.__manual_path = manual_path
        self.__handlers: list[Callable] = []

    def build(self):
        application = FastAPI(
            lifespan=self.__lifespan,
            title=self.__title,
            description=self.__description,
            docs_url=f"{SETTINGS.API_PREFIX}/docs",
            redoc_url=f"{SETTINGS.API_PREFIX}/redoc",
            openapi_url=f"{SETTINGS.API_PREFIX}/openapi.json"
        )

        application.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        application.include_router(router=base_router)
        # self.register_exception_handlers(application)

        return application

    def register_handlers(self, handlers: list[Callable]):
        self.__handlers = [handler for handler in handlers if handler not in self.__handlers]

    @asynccontextmanager
    async def __lifespan(self, app: FastAPI):
        await self.__on_startup()
        yield
        await self.__on_shutdown()

    async def __on_startup(self):
        await self.__set_service_params()
        for handler in self.__handlers:
            handler()

    async def __on_shutdown(self):
        ...

    async def __set_service_params(self):
        dm.set_title(self.__title)
        dm.set_address(self.__address)
        dm.set_description(self.__description)
        dm.set_manual_path(self.__manual_path)
