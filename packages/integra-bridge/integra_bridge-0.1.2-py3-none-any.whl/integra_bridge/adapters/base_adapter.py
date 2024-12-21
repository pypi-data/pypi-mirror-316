from abc import ABC, abstractmethod

from integra_bridge.common.enums import AdapterType


class BaseAdapter(ABC):
    _adapters: dict[str, set] = dict()

    def __init__(self):
        self.__view = None

    @abstractmethod
    async def get_view(self):
        ...

    @property
    def view(self):
        return self.__view

    @classmethod
    def get_adapters(cls, adapter_type: AdapterType) -> set:
        return cls._adapters.get(adapter_type.value, set())

    @classmethod
    def add_adapter(cls, service, adapter_type: AdapterType):
        group = cls._adapters.get(adapter_type.value, None)
        if group:
            group.add(service)
        else:
            cls._adapters[adapter_type.value] = {service, }

    @classmethod
    def remove_adapter(cls, service, adapter_type: AdapterType):
        group = cls._adapters.get(adapter_type.value, None)
        if group:
            group.remove(service)
