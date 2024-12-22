from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Annotated, Union
from ecoki.common.base_classes import PipelineTopologyInformation, PipelineInformationWithValues, BuildingBlockInformation, ConnectionInformation, ExecutionStatus, PipelineInformation
from ecoki.common.pipeline_pool_responses import PipelineTypes, PipelineMetaDataResponse, PipelineContentResponse
from ecoki.pipeline_framework.topology_provider.topology_provider_from_json import TopologyProviderFromJSON
from ecoki.pipeline_framework.topology_provider.topology_provider_from_dict import TopologyProviderFromDict
from ecoki.pipeline_framework.pipeline import Pipeline
import importlib
import requests
import json


class PipelineInformationResponse(BaseModel):
    payload: Union[PipelineInformationWithValues, dict] = {}
    execution_status: ExecutionStatus = ExecutionStatus()
    
class GetTopologyResponse(BaseModel):
    payload: Union[dict, PipelineInformation] = {}
    execution_status: ExecutionStatus = ExecutionStatus()

class RunPipelineResponse(BaseModel):
    payload: dict = {}
    execution_status: ExecutionStatus = ExecutionStatus()

class AddNodeResponse(BaseModel):
    payload: Union[BuildingBlockInformation, dict] = {}
    execution_status: ExecutionStatus = ExecutionStatus()

add_node_body_examples = {
    'example_building_block': {
        'summary': 'Example building block with no visualization',
        'description': 'Data split building block',
        'value': {
            'name': 'bb_data_split',
            'description': 'Data split into training and test subsets',
            'category': 'DataPreprocessing',
            'building_block_class': 'SplitTrainTest',
            'building_block_module': 'ecoki.building_blocks.code_based.modelling.build_and_train_model.split_traintest.split_traintest',
            'executor_module': 'ecoki.building_block_framework.building_block_executor.local_building_block_executor',
            'executor_class': 'LocalBuildingBlockExecutor',
            'visualizer_module': '',
            'visualizer_class': ''
            }
        }
    }

class RemoveBuildingBlockResponse(BaseModel):
    payload: dict = {}
    execution_status: ExecutionStatus = ExecutionStatus()
    
class AddConnectionResponse(BaseModel):
    payload: Union[ConnectionInformation, dict] = {}
    execution_status: ExecutionStatus = ExecutionStatus()
    
add_connection_body_examples = {
    'example_connection': {
        'name': 'Example connection',
        'description': 'Simple connection',
        'value': {
            'name': 'new_connection',
            'from_node': 'bb_data_split',
            'from_port': 'output_data',
            'to_node': 'bb_data_split',
            'to_port': 'output_data'
            }
        }
    }

class RemoveConnectionResponse(BaseModel):
    payload: dict = {}
    execution_status: ExecutionStatus = ExecutionStatus()

class RunWithArgumentsBody(BaseModel):
    inputs: list = []
    outputs: list = []


run_with_args_example = {
    'run_with_arguments': {
        'summary': 'Example of a structure to run the pipeline with argumens',
        'description': 'Example',
        'value': {
            'inputs': [
                {'building_block': 'conveyor_1',
                'inlet': 'input_data',
                'value': 'data'}
                ],
            'outputs': [
                {'building_block': 'conveyor_2',
                'outlet': 'output_data'}
                ],
        }
        }
    }
    
class RunWithArgsResponse(BaseModel):
    payload: list = []
    execution_status: ExecutionStatus = ExecutionStatus()
    
class PipelineRouter:
    def __init__(self, pipeline_manager, pipeline_pool_hostname, pipeline_pool_port):
        self.pipeline_manager = pipeline_manager
        self.pipeline_pool_hostname = pipeline_pool_hostname
        self.pipeline_pool_port = pipeline_pool_port
        self.router = APIRouter(tags=['Pipeline'])
        self.router.add_api_route('/pipelines/{pipeline_name}', self.get_pipeline_info, methods=['GET'], summary='Get pipeline information including values of ports', response_model=PipelineInformationResponse)
        self.router.add_api_route('/pipelines/{pipeline_name}/topology', self.get_topology, methods=['GET'], summary='Get pipeline topology', response_model=GetTopologyResponse)
        self.router.add_api_route('/pipelines/{pipeline_name}/run', self.run_pipeline, methods=['POST'], summary='Run pipeline', response_model=RunPipelineResponse)
        self.router.add_api_route('/pipelines/{pipeline_name}/run_interactive', self.run_pipeline_interactive, methods=['POST'], summary='Run pipeline interactive', response_model=RunPipelineResponse)
        self.router.add_api_route('/pipelines/{pipeline_name}/node', self.add_node, methods=['PUT'], summary='Add building block', response_model=AddNodeResponse)
        self.router.add_api_route('/pipelines/{pipeline_name}/node', self.delete_node, methods=['DELETE'], summary='Remove building block', response_model=RemoveBuildingBlockResponse)
        self.router.add_api_route('/pipelines/{pipeline_name}/connection', self.add_connection, methods=['PUT'], summary='Add connection', response_model=AddConnectionResponse)
        self.router.add_api_route('/pipelines/{pipeline_name}/connection', self.delete_connection, methods=['DELETE'], summary='Remove connection', response_model=RemoveConnectionResponse)
        self.router.add_api_route('/pipelines/{pipeline_name}/run_with_args', self.run_pipeline_with_args, methods=['POST'], summary='Run pipeline with arguments', response_model=RunWithArgsResponse)
        self.router.add_api_route('/pipelines/{pipeline_type}/{pipeline_name}', self.pipeline_pool_get_pipeline_info,
                                  methods=['GET'], response_model=PipelineMetaDataResponse)
        self.router.add_api_route('/pipelines/{pipeline_type}/{pipeline_name}/content',
                                  self.pipeline_pool_get_pipeline_topology,
                                  methods=['GET'], response_model=PipelineContentResponse)
        self.router.add_api_route('/pipelines/{pipeline_type}/update/{pipeline_name}/content',
                                  self.pipeline_pool_update_pipeline_topology,
                                  methods=['PUT'], response_model=PipelineContentResponse)
    
    async def get_pipeline_info(self, pipeline_name:str):
        """
        Get information about an pipeline
        """
        pipeline = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        if pipeline:
            return PipelineInformationResponse(payload=pipeline.get_info_obj(), execution_status=ExecutionStatus(command='get_pipeline_info', status=1, message='OK'))
        else:
            return PipelineInformationResponse(execution_status=ExecutionStatus(command='get_pipeline_info', status=1, message=f'Pipeline {pipeline_name} does not exist'))

    async def get_topology(self, pipeline_name:str):
        """
        Get topology information about an pipeline
        """
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        if pipeline_executor:
            return GetTopologyResponse(payload=pipeline_executor.get_topology_info_obj(),
                                        execution_status=ExecutionStatus(command='get_topology', status=0, message=f'OK'))
        else:
            return GetTopologyResponse(execution_status=ExecutionStatus(command='get_topology', status=1, message=f'Pipeline {pipeline_name} does not exist'))
        
    async def run_pipeline(self, pipeline_name:str):
        """
        Run pipeline
        """
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        if pipeline_executor:
            pipeline_executor.deactivate_interactive_mode()
            self.pipeline_manager.pipeline_thread_manager.run_thread(pipeline_name)  # run pipeline in a separate thread
            return RunPipelineResponse(execution_status=ExecutionStatus(command='run_pipeline', status=0, message=f'Pipeline {pipeline_name} is run'))
        else:
            return RunPipelineResponse(execution_status=ExecutionStatus(command='run_pipeline', status=1, message=f'Pipeline {pipeline_name} does not exist'))

    async def run_pipeline_interactive(self, pipeline_name:str):
        """
        Run pipeline interactively
        """
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        if pipeline_executor:
            pipeline_executor.create_interactive_gui()
            self.pipeline_manager.pipeline_thread_manager.run_thread(pipeline_name)  # run pipeline in a separate thread
            return RunPipelineResponse(execution_status=ExecutionStatus(command='run_pipeline', status=0, message=f'Pipeline {pipeline_name} is run'))
        else:
            return RunPipelineResponse(execution_status=ExecutionStatus(command='run_pipeline', status=1, message=f'Pipeline {pipeline_name} does not exist'))
    
    async def add_node(self, pipeline_name:str, building_block_add_body: Annotated[BuildingBlockInformation, Body(examples=add_node_body_examples)]):
        """
        Add building block
        """
        if not self.pipeline_manager.pipeline_exists(pipeline_name):
            return AddNodeResponse(execution_status=ExecutionStatus(command='add_node', status=1, message=f'Pipeline {pipeline_name} does not exist'))
            
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        add_success = pipeline_executor.add_node(node=building_block_add_body)
        if not add_success:
            return AddNodeResponse(execution_status=ExecutionStatus(command='add_node', status=2, message=f'Node {building_block_add_body.name} cannot be added to pipeline {pipeline_name}'))
        
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        return AddNodeResponse(payload=pipeline_executor.get_executor(building_block_add_body.name).get_info_obj(),
                                execution_status=ExecutionStatus(command='add_node', status=0, message=f'Node {building_block_add_body.name} added to pipeline {pipeline_name}'))
        
    async def delete_node(self, pipeline_name:str, building_block_name:str):
        """
        Delete building block
        """
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        if pipeline_executor is None:
            return RemoveBuildingBlockResponse(execution_status=ExecutionStatus(command='delete_node', status=1, message=f'Node {building_block_name} could not be removed, pipeline {pipeline_name} does not exist'))
        
        delete_success = pipeline_executor.delete_node(building_block_name)
        if not delete_success:
            return RemoveBuildingBlockResponse(execution_status=ExecutionStatus(command='delete_node', status=2, message=f'Node {building_block_name} could not be removed from pipeline {pipeline_name}, node {building_block_name} does not exist'))

        return RemoveBuildingBlockResponse(execution_status=ExecutionStatus(command='delete_node', status=0, message=f'Node {building_block_name} removed from pipeline {pipeline_name}'))
            
    
    async def add_connection(self, pipeline_name:str, connection_add_body: Annotated[ConnectionInformation, Body(examples=add_connection_body_examples)]):
        """
        Add connection
        """
        connection_name = connection_add_body.name
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        if pipeline_executor is None:
            return AddConnectionResponse(execution_status=ExecutionStatus(command='add_connection', status=1, message=f'Connection {connection_name} could not be added, pipeline {pipeline_name} does not exist'))
        
        add_success = pipeline_executor.add_connection(connection_add_body)
        if not add_success:
            return AddConnectionResponse(execution_status=ExecutionStatus(command='add_connection', status=3, message=f'Connection {connection_name} could not be added to pipeline {pipeline_name}'))
        
        return AddConnectionResponse(payload=pipeline_executor.pipeline.get_connection(connection_name).get_info_obj(),
                                    execution_status=ExecutionStatus(command='add_connection', status=0, message=f'Connection {connection_name} added to pipeline {pipeline_name}'))
        
        
    async def delete_connection(self, pipeline_name:str, connection_name: str):
        """
        Delete connection
        """
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        if pipeline_executor is None:
            return RemoveConnectionResponse(payload={},
                                            execution_status=ExecutionStatus(command='delete_connection', status=1, message=f'Connection {connection_name} could not be removed, pipeline {pipeline_name} does not exist'))
        
        delete_success = pipeline_executor.delete_connection(connection_name)
        if not delete_success:
            return RemoveConnectionResponse(payload={},
                                            execution_status=ExecutionStatus(command='delete_connection', status=3, message=f'Connection {connection_name} could not be removed from pipeline {pipeline_name}, connection {connection_name} does not exist'))

        return RemoveConnectionResponse(payload={},
                                            execution_status=ExecutionStatus(command='delete_connection', status=0, message=f'Connection {connection_name} removed from pipeline {pipeline_name}'))

    async def run_pipeline_with_args(self, pipeline_name:str, run_args_body: Annotated[RunWithArgumentsBody, Body(examples=run_with_args_example)]):
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        if not pipeline_executor:
            return RunWithArgsResponse(execution_status=ExecutionStatus(command='run_pipeline_with_args', status=1, message=f'Pipeline {pipeline_name} does not exist'))

        output_values = pipeline_executor.run_with_args(run_args_body.dict(), self.pipeline_manager)
        return RunWithArgsResponse(payload=output_values,
                                    execution_status=ExecutionStatus(command='run_pipeline_with_args', status=0, message=f'Pipeline {pipeline_name} is run'))

    async def pipeline_pool_get_pipeline_info(self, pipeline_type: PipelineTypes, pipeline_name: str):
        res = requests.get(f"http://{self.pipeline_pool_hostname}:{self.pipeline_pool_port}/api/v1/pipelines/{pipeline_type.value}/{pipeline_name}")
        return PipelineMetaDataResponse.parse_obj(res.json())

    async def pipeline_pool_get_pipeline_topology(self, pipeline_type: PipelineTypes, pipeline_name: str):
        res = requests.get(f"http://{self.pipeline_pool_hostname}:{self.pipeline_pool_port}/api/v1/pipelines/{pipeline_type.value}/{pipeline_name}/content")
        return PipelineContentResponse.parse_obj(res.json())

    async def pipeline_pool_update_pipeline_topology(self, pipeline_type: PipelineTypes, pipeline_name: str, pipeline_content_updated: dict, pipeline_new_name: str = None, overwrite: bool = True):
        res = requests.put(f"http://{self.pipeline_pool_hostname}:{self.pipeline_pool_port}/api/v1/pipelines/{pipeline_type.value}/update/{pipeline_name}/content",
                           params={"pipeline_new_name": pipeline_new_name, "overwrite": overwrite}, json=pipeline_content_updated)
        return PipelineContentResponse.parse_obj(res.json())
