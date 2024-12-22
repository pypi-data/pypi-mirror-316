from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Annotated
from ecoki.common.base_classes import  BuildingBlockInformationWithPorts, ExecutionStatus


class GetValuesResponse(BaseModel):
    payload: BuildingBlockInformationWithPorts = BuildingBlockInformationWithPorts()
    execution_status: ExecutionStatus = ExecutionStatus()


class BuildingBlockRouter:
    def __init__(self, pipeline_manager):
        self.pipeline_manager = pipeline_manager
        self.router = APIRouter(tags=['Building Block'])
        self.router.add_api_route('/pipelines/{pipeline_name}/nodes/{node_name}', self.get_node_info, methods=['GET'], summary='Get node info')
        self.router.add_api_route('/pipelines/{pipeline_name}/nodes/{node_name}/values', self.get_node_values, methods=['GET'],
                                  summary='Get node values')
    
    async def get_node_values(self, pipeline_name:str, node_name:str):
        pipeline = self.pipeline_manager.get_pipeline(pipeline_name=pipeline_name)
        if not pipeline:
            return GetValuesResponse(execution_status=ExecutionStatus(command='get_node_values', status=1, message=f'Pipeline {pipeline_name} does not exist'))
        
        node = pipeline.get_node(node_name)
        if not node:
            return GetValuesResponse(execution_status=ExecutionStatus(command='get_node_values', status=2, message=f'In pipeline {pipeline_name} there is no node with name {node_name}'))
        
        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        return GetValuesResponse(payload=pipeline_executor.get_executor(node_name).get_info_obj_with_values(),
                                execution_status=ExecutionStatus(command='get_node_values', status=0, message=f'OK'))

    async def get_node_info(self, pipeline_name: str, node_name: str):
        pipeline = self.pipeline_manager.get_pipeline(pipeline_name=pipeline_name)
        if not pipeline:
            return GetValuesResponse(execution_status=ExecutionStatus(command='get_node_info', status=1,
                                                                      message=f'Pipeline {pipeline_name} does not exist'))

        node = pipeline.get_node(node_name)
        if not node:
            return GetValuesResponse(execution_status=ExecutionStatus(command='get_node_info', status=2,
                                                                      message=f'In pipeline {pipeline_name} there is no node with name {node_name}'))

        pipeline_executor = self.pipeline_manager.get_pipeline_executor(pipeline_name=pipeline_name)
        return GetValuesResponse(payload=pipeline_executor.get_executor(node_name).get_info_obj(),
                                 execution_status=ExecutionStatus(command='get_node_info', status=0, message=f'OK'))
