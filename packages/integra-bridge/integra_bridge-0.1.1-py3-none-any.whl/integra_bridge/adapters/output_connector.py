from abc import ABC

from integra_bridge.adapters.base_adapter import BaseAdapter
from integra_bridge.common.enums import AdapterType

from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.entity.connector import Connector
from integra_bridge.entity.output_status import OutputStatus


class OutputConnectorAdapter(BaseAdapter, ABC):

    def __init__(self):
        super().__init__()
        self.__view = None
        BaseAdapter.add_adapter(self, adapter_type=AdapterType.connectors)

    def __del__(self):
        BaseAdapter.remove_adapter(self, adapter_type=AdapterType.connectors)

    async def pull_from_integra(self, input_body: dict, params: dict, headers: dict) -> OutputStatus:
        status = OutputStatus()
        return status

    async def validate_output(self, connector: Connector) -> ValidationResponse:
        return ValidationResponse(result=True)
