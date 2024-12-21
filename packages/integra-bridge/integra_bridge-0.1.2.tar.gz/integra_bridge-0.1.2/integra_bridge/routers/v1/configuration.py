from fastapi.responses import FileResponse

from integra_bridge.api_router import APIRouter
from integra_bridge.dto.responces.external_service import ExternalServiceConfigResponse
from integra_bridge.common.dependency_manager import dm
from integra_bridge.services.configuration import ConfigurationHandler

configuration_router = APIRouter(prefix='/configuration', tags=["Работа с конфигурациями внешних сервисов"])


@configuration_router.get(
    path='/',
    response_model=ExternalServiceConfigResponse,
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def get_configurations() -> ExternalServiceConfigResponse:
    return await ConfigurationHandler.get_configurations()


@configuration_router.get(
    path='/manual'
)
async def get_manual():
    manual_path = dm.manual_path
    if manual_path.exists():
        return FileResponse(manual_path, media_type='application/octet-stream', filename=dm.manual_path.name)
    else:
        return {"error": "File not found"}
