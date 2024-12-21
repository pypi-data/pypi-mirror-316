from integra_bridge.adapters.base_adapter import BaseAdapter

from integra_bridge.common.dependency_manager import dm
from integra_bridge.dto.responces.external_service import ExternalServiceConfigResponse


class ConfigurationHandler:

    @classmethod
    async def get_configurations(cls):

        from integra_bridge.common.enums import AdapterType
        processors = BaseAdapter.get_adapters(adapter_type=AdapterType.processors)
        processor_views = []
        for processor in processors:
            processor_view = await processor.get_view()
            processor_views.append(processor_view)

        connectors = BaseAdapter.get_adapters(adapter_type=AdapterType.connectors)
        connector_views = []
        for connector in connectors:
            connector_view = await connector.get_view()
            connector_views.append(connector_view)

        response = ExternalServiceConfigResponse(
            service_name=dm.title,
            service_address=dm.address,
            application_start_date=dm.application_start_date,
            processor_views=processor_views,
            connector_views=connector_views,
            manual_file_name=dm.manual_path.name
        )
        return response
