from pydantic import BaseModel
from typing import Union
from enum import Enum
from ecoki.common.base_classes import PipelineInformation, ExecutionStatus


class PipelineTypes(str, Enum):
    ecoki_pipelines = "ecoki"
    custom_pipelines = "custom"


class PipelineSettingsMetaData(BaseModel):
    short_description: str = "undefined"
    description: str = "undefined"
    example: str = "undefined"
    version: str = "undefined"
    category: list = []
    inputs: dict = {}
    outputs: dict = {}


class PipelineMetaData(PipelineSettingsMetaData):
    name: str
    type: str
    building_blocks: list = []


class PipelineAddUpdateInformation(PipelineInformation):
    metadata: PipelineSettingsMetaData


#  -----------------  Response models of pipeline pool ---------------------
class PipelineListResponse(BaseModel):
    payload: dict[str, Union[list, None]] = {}
    execution_status: ExecutionStatus = ExecutionStatus()


class PipelineMetaDataResponse(BaseModel):
    payload: Union[dict, PipelineMetaData] = {}
    execution_status: ExecutionStatus = ExecutionStatus()


class PipelineContentResponse(BaseModel):
    payload: Union[dict, PipelineInformation] = {}
    execution_status: ExecutionStatus = ExecutionStatus()


class PipelineAddUpdateResponse(BaseModel):
    payload: PipelineAddUpdateInformation
    execution_status: ExecutionStatus = ExecutionStatus()


class DeletePipelineResponse(BaseModel):
    payload: dict = {}
    execution_status: ExecutionStatus = ExecutionStatus()


class FilterPipelineResponse(BaseModel):
    payload: list = []
    execution_status: ExecutionStatus = ExecutionStatus()
