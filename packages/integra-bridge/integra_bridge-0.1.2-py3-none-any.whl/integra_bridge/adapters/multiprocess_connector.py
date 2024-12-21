import asyncio
from abc import ABC
from typing import Any

import orjson

from integra_bridge.adapters.base_input_connector import BaseInputConnectorAdapter
from integra_bridge.dto import Exchange, ConnectorToBlockView
from integra_bridge.dto.body import Body
from integra_bridge.dto.redeploy import ConnectionParams


class MultiprocessInputConnectorAdapter(BaseInputConnectorAdapter, ABC):
    """
    Данный тип коннекторов предназначен для работы в многопоточной среде. Данные о всех зарегистрированных инстансах
    перенаправляются методами on_after_deploy и on_after_redeploy для описания логики хранения и обработки с
    использованием СУБД.
    """

    @classmethod
    async def push_to_integra(cls, input_body: Any, connect_to_block_id: str, *args: Any, **kwargs: Any):
        url_integra_service = kwargs.get('url_integra_service')
        if not url_integra_service:
            raise Exception('url_integra_service is not defined')

        try:
            string_body = orjson.dumps(input_body).decode(encoding="utf-8")
            body_type = "json"
        except Exception:
            string_body = input_body
            body_type = "string"

        input_body = Body(stringBody=string_body, type=body_type)
        exchange = Exchange(inputBody=input_body)

        try:
            company_id, block_id, connect_id = connect_to_block_id.split('_')
            exchange.block_id = block_id
            exchange.input_connect_id = connect_id
            exchange.company_id = company_id
        except Exception:
            raise Exception(f'connect_to_block_id have wrong format: {connect_to_block_id}')

        return await cls._send(exchange, url_integra_service)

    async def deploy_input_flow(self, exchange: Exchange, connector_title: str, *args: Any, **kwargs: Any) -> int:
        connector_to_block_view = ConnectorToBlockView(
            connector_title=connector_title,
            company_id=exchange.company_id,
            block_id=exchange.block_id,
            connect_id=exchange.input_connect_id,
            url_integra_service=exchange.headers.get('urlIntegra'),
            exchange_deploy=exchange
        )
        connector_to_block_id = await connector_to_block_view.get_id()
        connector_url = f"{connector_to_block_view.url_integra_service}/api/external/connector/input/{connector_to_block_id}?connectorTitle={connector_to_block_view.connector_title}"
        connection_params = exchange.input_connect.params or {}

        # ВРЕМЕННАЯ ЗАГЛУШКА
        connection_auth = {}

        print('!!!!!!!!DEPLOYED:', connector_to_block_view)

        asyncio.create_task(self.on_after_deploy(
            connection_id=connector_to_block_id,
            connection_params=connection_params,
            connector_url=connector_url,
            auth=connection_auth
        ))
        return exchange

    async def redeploy_input_flow(self, connection_params: ConnectionParams, connector_title: str, *args: Any,
                                  **kwargs: Any):
        connector_to_block_view = ConnectorToBlockView(
            connector_title=connector_title,
            company_id=connection_params.company_id,
            block_id=connection_params.block_id,
            connect_id=connection_params.connect_id,
            url_integra_service=connection_params.url_integra_service,
        )
        connector_to_block_id = await connector_to_block_view.get_id()
        connector_url = f"{connector_to_block_view.url_integra_service}/api/external/connector/input/{connector_to_block_id}?connectorTitle={connector_to_block_view.connector_title}"
        print('!!!!!!!!REDEPLOYED:', connector_to_block_view)
        asyncio.create_task(self.on_after_redeploy(
            connection_id=connector_to_block_id,
            connection_params=connection_params.params,
            connector_url=connector_url,
            auth=connection_params.auth
        ))

    async def destroy_input_flow(self, exchange: Exchange, connector_title: str, *args: Any, **kwargs: Any):
        connector_to_block_view = ConnectorToBlockView(
            connector_title=connector_title,
            company_id=exchange.company_id,
            block_id=exchange.block_id,
            connect_id=exchange.input_connect_id,
            exchange_deploy=exchange
        )
        connector_to_block_id = await connector_to_block_view.get_id()
        print('!!!!!!!!DEPLOYED:', connector_to_block_view)
        asyncio.create_task(self.on_after_destroy(
            connection_id=connector_to_block_id,
            connection_params=connector_to_block_view.model_dump()
        ))
        return exchange
