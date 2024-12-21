from abc import ABC
from typing import Any

import orjson

from integra_bridge.adapters.base_input_connector import BaseInputConnectorAdapter
from integra_bridge.dto import Exchange, ConnectorToBlockView
from integra_bridge.dto.body import Body


class SingleModeInputConnectorAdapter(BaseInputConnectorAdapter, ABC):
    """
    Данный простой тип коннекторов предназначен для работы в однопоточной среде. Данные о всех зарегистрированных
    инстансах хранятся в оперативной памяти. Не подойдет при работе в кластере или использовании нескольких воркеров.
    """

    _connector_to_block_views: dict[str, ConnectorToBlockView] = {}

    @classmethod
    async def push_to_integra(cls, input_body: Any, connect_to_block_id: str, *args: Any, **kwargs: Any) -> int:
        try:
            string_body = orjson.dumps(input_body).decode(encoding="utf-8")
            body_type = "json"
        except Exception:
            string_body = input_body
            body_type = "string"

        connector_to_block_view = SingleModeInputConnectorAdapter._connector_to_block_views.get(connect_to_block_id)
        if not connector_to_block_view:
            raise ValueError(f"connect to block view {connect_to_block_id} not found")

        input_body = Body(stringBody=string_body, type=body_type)
        exchange = Exchange(inputBody=input_body)
        exchange.block_id = connector_to_block_view.block_id
        exchange.input_connect_id = connector_to_block_view.connect_id
        exchange.company_id = connector_to_block_view.company_id

        url = f"{connector_to_block_view.url_integra_service}/api/external/connector/input/{connect_to_block_id}?connectorTitle={connector_to_block_view.connector_title}"
        return await cls._send(exchange, url)

    async def deploy_input_flow(self, exchange: Exchange, connector_title: str, *args: Any, **kwargs: Any):
        connector_to_block_view = ConnectorToBlockView(
            connector_title=connector_title,
            company_id=exchange.company_id,
            block_id=exchange.block_id,
            connect_id=exchange.input_connect_id,
            url_integra_service=exchange.headers.get('urlIntegra'),
            exchange_deploy=exchange
        )
        connector_to_block_id = await connector_to_block_view.get_id()
        connection_params = exchange.input_connect.params or {}
        SingleModeInputConnectorAdapter._connector_to_block_views[connector_to_block_id] = connector_to_block_view
        print('!!!!!!!!DEPLOYED:',
              SingleModeInputConnectorAdapter._connector_to_block_views[connector_to_block_id].connector_title,
              SingleModeInputConnectorAdapter._connector_to_block_views.keys())
        await self.on_after_deploy(
            connection_id=connector_to_block_id,
            connection_params=connection_params
        )
        return exchange

    async def redeploy_input_flow(self, connector_params: dict, connector_title: str, *args: Any, **kwargs: Any):
        connector_to_block_view = ConnectorToBlockView(
            connector_title=connector_title,
            company_id=connector_params.get('companyId'),
            block_id=connector_params.get('blockId'),
            connect_id=connector_params.get('connectId'),
            url_integra_service=connector_params.get('urlIntegraService'),
        )
        connector_to_block_id = await connector_to_block_view.get_id()
        connection_params = connector_params.get('params', {})
        SingleModeInputConnectorAdapter._connector_to_block_views[connector_to_block_id] = connector_to_block_view
        print('!!!!!!!!REDEPLOYED:',
              SingleModeInputConnectorAdapter._connector_to_block_views[connector_to_block_id].connector_title,
              SingleModeInputConnectorAdapter._connector_to_block_views.keys())
        await self.on_after_redeploy(
            connection_id=connector_to_block_id,
            connection_params=connection_params
        )

    async def destroy_input_flow(self, exchange: Exchange, connector_title: str, *args: Any, **kwargs: Any):
        connector_to_block_view = ConnectorToBlockView(
            connector_title=connector_title,
            company_id=exchange.company_id,
            block_id=exchange.block_id,
            connect_id=exchange.input_connect_id,
            exchange_deploy=exchange
        )
        connector_to_block_id = await connector_to_block_view.get_id()
        SingleModeInputConnectorAdapter._connector_to_block_views.pop(connector_to_block_id, None)
        print('!!!!!!!!DESTROYED:', SingleModeInputConnectorAdapter._connector_to_block_views.keys())
        await self.on_after_destroy(
            connection_id=connector_to_block_id,
            connector_params=connector_to_block_view.model_dump()
        )
        return exchange
