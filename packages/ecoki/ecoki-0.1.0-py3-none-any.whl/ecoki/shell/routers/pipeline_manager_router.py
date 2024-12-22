from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Annotated, Union
from ecoki.common.base_classes import ExecutionStatus, PipelineManagerInformation, PipelineInformation, PipelineTopologyInformation
from ecoki.common.pipeline_pool_responses import PipelineTypes, PipelineListResponse, PipelineContentResponse, DeletePipelineResponse, FilterPipelineResponse, PipelineAddUpdateInformation
from ecoki.pipeline_framework.topology_provider.topology_provider_from_json import TopologyProviderFromJSON
import requests
import json


class ActivePipelineListResponse(BaseModel):
    payload: Union[PipelineManagerInformation, dict] = {}
    execution_status: ExecutionStatus = ExecutionStatus()


class AddPipelineResponse(BaseModel):
    payload: PipelineInformation = PipelineInformation()
    execution_status: ExecutionStatus = ExecutionStatus()


add_pipeline_body_examples = {
    'empty_pipeline': {
        'summary': 'Empty pipeline',
        'description': '',
        'value': {
            'name': 'Empty pipeline',
            'description': 'This is a an empty pipeline with no nodes and connections',
            'version': '0.0.0',
            'topology':
                {
                    'nodes': [],
                    'connections': []
                 },
            'executor_module': 'ecoki.pipeline_framework.pipeline_executor.local_pipeline_executor',
            'executor_class': 'LocalPipelineExecutor'
            }
        }
    }

class RemovePipelinePayload(BaseModel):
    pipeline_name: str = ''

class RemovePipelineResponse(BaseModel):
    payload: Union[RemovePipelinePayload, dict] = {}
    execution_status: ExecutionStatus = ExecutionStatus()


class PipelineManagerRouter:
    def __init__(self, pipeline_manager, pipeline_pool_hostname: str, pipeline_pool_port: int):
        self.pipeline_manager = pipeline_manager
        self.pipeline_pool_hostname = pipeline_pool_hostname
        self.pipeline_pool_port = pipeline_pool_port
        self.router = APIRouter(tags=['Pipeline Manager'])
        self.router.add_api_route('/pipelines/', self.get_pipeline_list, methods=['GET'], summary='Get list of all active pipelines', response_model=ActivePipelineListResponse)
        # self.router.add_api_route('/pipelines/', self.add_pipeline, methods=['PUT'], summary='Create a pipeline', response_model=AddPipelineResponse)
        self.router.add_api_route('/pipelines/', self.delete_pipeline, methods=['DELETE'], summary='Delete a pipeline from ecoKI platform', response_model=RemovePipelineResponse)
        self.router.add_api_route('/pipelines/', self.pipeline_pool_create_pipeline, methods=['PUT'], summary='Pipeline Pool create a pipeline',
                                  response_model=AddPipelineResponse)
        self.router.add_api_route('/pipelines/{pipeline_type}/overview', self.pipeline_pool_get_pipelines_list,
                                  methods=['GET'], response_model=PipelineListResponse)
        self.router.add_api_route('/pipelines/custom/add/{pipeline_name}/content',
                                  self.pipeline_pool_add_custom_pipeline,
                                  methods=['POST'], response_model=PipelineContentResponse)
        self.router.add_api_route('/pipelines/custom/delete/{pipeline_name}',
                                  self.pipeline_pool_delete_custom_pipeline,
                                  methods=['DELETE'], response_model=DeletePipelineResponse)
        self.router.add_api_route('/pipelines/{pipeline_type}/filter/{pipeline_name}',
                                  self.pipeline_pool_filter_pipelines,
                                  methods=['GET'], response_model=FilterPipelineResponse)

    async def get_pipeline_list(self):
        """
        Get a list of pipelines
        """
        return ActivePipelineListResponse(payload={'pipelines': self.pipeline_manager.get_info_obj()},
                                    execution_status=ExecutionStatus(command='get_pipeline_list', status=1, message='OK'))

    async def add_pipeline(self, pipeline_add_body: Annotated[PipelineInformation, Body(examples=add_pipeline_body_examples)]):
        """
        Add a pipeline
        """
        # toDO can be removed !!!
        topology_provider=TopologyProviderFromJSON(pipeline_add_body.topology)
        """
        the pipeline executor module should be extracted in the pipeline manager, not here, so I moved the lines that are commented out into the pipeline manager
        """
        add_success = self.pipeline_manager.add_pipeline(pipeline_name=pipeline_add_body.name,
                                                         pipeline_execution_mode=pipeline_add_body.execution_mode,
                                                         topology_provider=topology_provider)
        if add_success:
            exec_status = ExecutionStatus(command='add_pipeline',
                                          code=0,
                                          message=f'Pipeline {pipeline_add_body.name} added')
        else:
            exec_status = ExecutionStatus(command='add_pipeline',
                                          code=1,
                                          message=f'Pipeline {pipeline_add_body.name} was not added because a pipeline with this name already exists')
        return AddPipelineResponse(payload=pipeline_add_body, execution_status=exec_status)

    async def delete_pipeline(self, pipeline_name):
        """
        Remove a pipeline by its ID
        """
        delete_success = self.pipeline_manager.delete_pipeline(pipeline_name=pipeline_name)
        if delete_success:
            exec_status = ExecutionStatus(command='delete_pipeline',
                                          code=0,
                                          message=f'Pipeline {pipeline_name} removed')
        else:
            exec_status = ExecutionStatus(command='delete_pipeline',
                                          code=1,
                                          message=f'Pipeline {pipeline_name} was not removed because does not exist')
        return AddPipelineResponse(payload=RemovePipelinePayload(pipeline_name=pipeline_name),
                                   execution_status=exec_status)

    async def pipeline_pool_create_pipeline(self, pipeline_type: PipelineTypes, pipeline_name: str):
        pipeline_content = requests.get(
            f"http://{self.pipeline_pool_hostname}:{self.pipeline_pool_port}/api/v1/pipelines/{pipeline_type.value}/{pipeline_name}/content")
        parsed_pipeline_content = pipeline_content.json()["payload"]
        topology = parsed_pipeline_content["topology"]
        topology_provider = TopologyProviderFromJSON(PipelineTopologyInformation(**topology))

        add_success = self.pipeline_manager.add_pipeline(pipeline_name=parsed_pipeline_content["name"],
                                                         pipeline_execution_mode=parsed_pipeline_content[
                                                             "execution_mode"], topology_provider=topology_provider, metadata=parsed_pipeline_content["metadata"])
        if add_success:
            exec_status = ExecutionStatus(command='add_pipeline',
                                          code=0,
                                          message=f'Pipeline {parsed_pipeline_content["name"]} added')
        else:
            exec_status = ExecutionStatus(command='add_pipeline',
                                          code=1,
                                          message=f'Pipeline {parsed_pipeline_content["name"]} was not added because a pipeline with this name already exists')
        return AddPipelineResponse(payload=PipelineInformation(**parsed_pipeline_content), execution_status=exec_status)

    async def pipeline_pool_get_pipelines_list(self, pipeline_type: PipelineTypes):
        res = requests.get(f"http://{self.pipeline_pool_hostname}:{self.pipeline_pool_port}/api/v1/pipelines/{pipeline_type.value}/overview")
        return PipelineListResponse.parse_obj(res.json())

    async def pipeline_pool_add_custom_pipeline(self, pipeline_name, pipeline_content: PipelineAddUpdateInformation, overwrite: bool = False):
        res = requests.post(
            f"http://{self.pipeline_pool_hostname}:{self.pipeline_pool_port}/api/v1/pipelines/custom/add/{pipeline_name}/content", params={"overwrite": overwrite}, json=pipeline_content.dict())
        return PipelineContentResponse.parse_obj(res.json())

    async def pipeline_pool_delete_custom_pipeline(self, pipeline_name: str):
        res = requests.delete(
            f"http://{self.pipeline_pool_hostname}:{self.pipeline_pool_port}/api/v1/pipelines/custom/delete/{pipeline_name}")
        return DeletePipelineResponse.parse_obj(res.json())

    async def pipeline_pool_filter_pipelines(self, pipeline_name: str, pipeline_type: PipelineTypes):
        res = requests.get(
            f"http://{self.pipeline_pool_hostname}:{self.pipeline_pool_port}/api/v1/pipelines/{pipeline_type.value}/filter/{pipeline_name}")
        return FilterPipelineResponse.parse_obj(res.json())
