from abc import ABC, abstractmethod
from typing import Any

import httpx
import orjson
from starlette import status

from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.adapters.base_adapter import BaseAdapter
from integra_bridge.common.enums import AdapterType
from integra_bridge.common.settings import SETTINGS
from integra_bridge.dto import Exchange
from integra_bridge.entity.connector import Connector


class BaseInputConnectorAdapter(BaseAdapter, ABC):

    def __init__(self):
        super().__init__()
        self.__view = None
        BaseAdapter.add_adapter(self, adapter_type=AdapterType.connectors)

    def __del__(self):
        BaseAdapter.remove_adapter(self, adapter_type=AdapterType.connectors)

    @abstractmethod
    async def push_to_integra(self, input_body: Any, connect_to_block_id: str, *args: Any, **kwargs: Any):
        ...

    @abstractmethod
    async def deploy_input_flow(self, exchange: Exchange, connector_title: str, *args: Any, **kwargs: Any):
        ...

    @abstractmethod
    async def destroy_input_flow(self, exchange: Exchange, connector_title: str, *args: Any, **kwargs: Any):
        ...

    @abstractmethod
    async def on_after_deploy(self, connection_id: str, connection_params: dict, connector_url: str | None = None,
                              auth: dict | None = None, *args: Any, **kwargs: Any) -> None:
        ...

    async def on_after_redeploy(self, connection_id: str, connection_params: dict, connector_url: str | None = None,
                                auth: dict | None = None, *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    async def on_after_destroy(self, connection_id: str, connection_params: dict, *args: Any, **kwargs: Any) -> None:
        ...

    async def redeploy_input_flow(self, connection_params: dict, connector_title: str, *args: Any, **kwargs: Any):
        ...

    async def validate_input(self, connector: Connector) -> ValidationResponse:
        return ValidationResponse(result=True)

    @classmethod
    async def _send(cls, exchange: Exchange, connector_url: str) -> int:
        auth = httpx.BasicAuth(username='admin', password='admin')
        async with httpx.AsyncClient(auth=auth, timeout=SETTINGS.DEFAULT_CONNECTOR_TIMEOUT) as client:
            try:
                response = await client.post(
                    connector_url,
                    content=orjson.dumps(exchange.model_dump(by_alias=True)),
                    headers={"Content-Type": "application/json"},
                    timeout=SETTINGS.DEFAULT_CONNECTOR_TIMEOUT
                )
            except httpx.TimeoutException:
                return status.HTTP_504_GATEWAY_TIMEOUT
            except ValueError as err:
                print('Error while sending to integra: ', str(err))
                return status.HTTP_406_NOT_ACCEPTABLE
            return response.status_code
