from abc import abstractmethod, ABC

from integra_bridge.adapters.base_adapter import BaseAdapter
from integra_bridge.dto import Exchange
from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.entity.processor import Processor
from integra_bridge.common.enums import AdapterType


class ProcessorAdapter(BaseAdapter, ABC):

    def __init__(self):
        super().__init__()
        self.__view = None
        BaseAdapter.add_adapter(self, adapter_type=AdapterType.processors)

    def __del__(self):
        BaseAdapter.remove_adapter(self, adapter_type=AdapterType.processors)

    @abstractmethod
    async def execute(self, input_body: dict, params: dict) -> dict:
        ...

    async def validate(self, processor: Processor) -> ValidationResponse:
        return ValidationResponse(result=True)
