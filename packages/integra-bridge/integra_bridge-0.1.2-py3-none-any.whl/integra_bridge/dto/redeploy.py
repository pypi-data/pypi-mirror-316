from pydantic import BaseModel, ConfigDict, StrictStr, Field


class ConnectionParams(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    company_id: StrictStr | None = Field(None, alias="companyId")
    block_id: StrictStr | None = Field(None, alias="blockId")
    connect_id: StrictStr | None = Field(None, alias="connectId")
    url_integra_service: StrictStr | None = Field(None, alias="urlIntegraService")
    params: dict = Field(default_factory=dict, alias="params")
    auth: dict = Field(default_factory=dict, alias="auth")


class RedeployConnectors(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    input_connectors: dict[str, list[ConnectionParams]] = Field(default_factory=dict, alias="inputConnectors")
