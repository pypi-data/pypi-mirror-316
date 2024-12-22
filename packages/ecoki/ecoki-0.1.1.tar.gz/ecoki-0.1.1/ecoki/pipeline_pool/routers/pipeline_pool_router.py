from fastapi import FastAPI, APIRouter
import json
import os
from typing import Union
from ecoki.common.base_classes import PipelineInformation, ExecutionStatus
from ecoki.common.pipeline_pool_responses import PipelineListResponse, PipelineMetaData, PipelineMetaDataResponse, PipelineTypes, \
    PipelineContentResponse, DeletePipelineResponse, FilterPipelineResponse, PipelineAddUpdateInformation, PipelineAddUpdateResponse
import shutil


def get_pipeline_folder_structure(pipeline_folder_path, content_type):
    pipeline_folder_list = []
    for item in os.listdir(f"{pipeline_folder_path}/{content_type}"):
        item_path = os.path.join(f"{pipeline_folder_path}/{content_type}", item)
        if os.path.isdir(item_path):
            pipeline_folder_list.append(item)
    return pipeline_folder_list


def check_pipeline_exists(pipeline_path):
    if not os.path.exists(pipeline_path):
        return False
    else:
        return True


def get_pipeline_metadata(pipeline_folder_path, pipeline_type, pipeline_name):
    pipeline_config_path = f'{pipeline_folder_path}/{pipeline_type}/{pipeline_name}/settings.json'

    if not check_pipeline_exists(pipeline_config_path):
        return False
    else:
        with open(pipeline_config_path) as pipeline_file:
            pipeline_contents_json = pipeline_file.read()
            pipeline_contents = json.loads(pipeline_contents_json)
        pipeline_meta_data = pipeline_contents["metadata"]
        topology = pipeline_contents["topology"]["nodes"]
        building_blocks = []
        for i in topology:
            building_blocks.append(i["building_block_class"])
        pipeline_meta_data.update(
            {"name": pipeline_contents["name"], "building_blocks": building_blocks, "type": pipeline_type})

        return pipeline_meta_data


def filter_pipelines(pipeline_folder_path, pipeline_type, pipeline_name_keyword):
    pipeline_list = get_pipeline_folder_structure(pipeline_folder_path, pipeline_type)
    filter_pipeline_list = []
    if pipeline_name_keyword in pipeline_list:
        filter_pipeline_list.append(pipeline_name_keyword)

    else:
        for pipeline in pipeline_list:
            if pipeline_name_keyword in pipeline.split("_"):
                filter_pipeline_list.append(pipeline)

    return filter_pipeline_list


class PipelinePoolRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Pipeline Pool'],
                                prefix="/pipelines")
        self.router.add_api_route("/{pipeline_type}/overview", self.get_pipeline_list,
                                  response_model=PipelineListResponse, methods=["GET"])
        self.router.add_api_route("/{pipeline_type}/{pipeline_name}", self.get_pipeline_meta_info,
                                  response_model=PipelineMetaDataResponse, methods=["GET"])
        self.router.add_api_route("/{pipeline_type}/{pipeline_name}/content", self.get_pipeline_content,
                                  response_model=PipelineContentResponse, methods=["GET"])
        self.router.add_api_route("/custom/add/{pipeline_name}/content", self.add_custom_pipeline,
                                  response_model=PipelineAddUpdateResponse, methods=["POST"])
        self.router.add_api_route("/{pipeline_type}/update/{pipeline_name}/content", self.update_pipeline,
                                  response_model=PipelineAddUpdateResponse, methods=["PUT"])
        self.router.add_api_route("/custom/delete/{pipeline_name}", self.delete_custom_pipeline,
                                  response_model=DeletePipelineResponse, methods=["DELETE"])
        #self.router.add_api_route("/{pipeline_type}/filter/{pipeline_name}", self.filter_pipelines_by_keyword,
        #                          response_model=FilterPipelineResponse, methods=["GET"])

        self.pipeline_root_folder = "ecoki/pipelines"

    async def get_pipeline_list(self, pipeline_type: PipelineTypes):
        #  get list of ecoki pipelines
        ecoki_pipeline_list = get_pipeline_folder_structure(self.pipeline_root_folder, pipeline_type.name)
        return PipelineListResponse(payload={pipeline_type.name: ecoki_pipeline_list},
                                    execution_status=ExecutionStatus(command=f'get list of all {pipeline_type.value} pipelines',
                                                                     status=0, message='OK'))

    async def get_pipeline_meta_info(self, pipeline_type: PipelineTypes, pipeline_name: str):
        # get metadata (description) of default/custom pipeline
        pipeline_folder = pipeline_type.name
        pipeline_category = pipeline_type.value
        pipeline_metadata = get_pipeline_metadata(self.pipeline_root_folder, pipeline_folder, pipeline_name)

        if not pipeline_metadata:
            return PipelineMetaDataResponse(
                execution_status=ExecutionStatus(command=f'get metadata of {pipeline_category} pipeline: '
                                                         f'{pipeline_name}',
                                                 status=1, message=f'{pipeline_category} pipeline '
                                                                   f'{pipeline_name} or its configuration file does not exist'))
        else:
            return PipelineMetaDataResponse(payload=PipelineMetaData.parse_obj(pipeline_metadata),
                                            execution_status=ExecutionStatus(
                                                command=f'get metadata of {pipeline_category} pipeline: '
                                                        f'{pipeline_name}',
                                                status=0, message='OK'))

    async def get_pipeline_content(self, pipeline_type: PipelineTypes, pipeline_name: str):
        pipeline_folder = pipeline_type.name
        pipeline_category = pipeline_type.value
        pipeline_config_path = f'{self.pipeline_root_folder}/{pipeline_folder}/{pipeline_name}/settings.json'

        if not check_pipeline_exists(pipeline_config_path):
            return PipelineContentResponse(
                execution_status=ExecutionStatus(command=f'get content of {pipeline_category} pipeline: '
                                                         f'{pipeline_name}',
                                                 status=1, message=f'{pipeline_category} pipeline '
                                                                   f'{pipeline_name} or its configuration file does not exist'))
        else:
            with open(pipeline_config_path) as pipeline_file:
                pipeline_contents = pipeline_file.read()
                pipeline_content_dict = json.loads(pipeline_contents)

                #del pipeline_content_dict["metadata"]

            return PipelineContentResponse(payload=PipelineInformation.parse_obj(pipeline_content_dict),
                                           execution_status=ExecutionStatus(
                                               command=f'get content of {pipeline_category} pipeline: '
                                                       f'{pipeline_name}',
                                               status=0, message='OK'))

    async def add_custom_pipeline(self, pipeline_name: str, pipeline_content: PipelineAddUpdateInformation,
                                  overwrite: bool = False):
        # ---------------- add a new custom pipeline  --------------------
        new_pipeline_path = f"{self.pipeline_root_folder}/custom_pipelines/{pipeline_name}"

        if check_pipeline_exists(new_pipeline_path):
            if not overwrite:
                return PipelineContentResponse(execution_status=ExecutionStatus(command='add a new custom pipeline',
                                                                                status=1, message='pipeline exists'))
        else:
            os.makedirs(new_pipeline_path)

        pipeline_dict = pipeline_content.dict()
        pipeline_json = json.dumps(pipeline_dict)

        with open(new_pipeline_path + "/settings.json", "w") as pipeline_file:
            print(6666, pipeline_json)
            pipeline_file.write(pipeline_json)
        return PipelineAddUpdateResponse(payload=PipelineAddUpdateInformation.parse_obj(pipeline_dict),
                                       execution_status=ExecutionStatus(command='add a new pipeline',
                                                                        status=0, message='OK'))

    async def update_pipeline(self, pipeline_name: str, pipeline_type: PipelineTypes, pipeline_content_updated: dict,
                              pipeline_new_name: str = None, overwrite: bool = False):
        #  change or update an existing default pipeline
        pipeline_path = f'{self.pipeline_root_folder}/{pipeline_type.name}/{pipeline_name}/settings.json'

        if not check_pipeline_exists(pipeline_path):
            return PipelineContentResponse(execution_status=ExecutionStatus(
                command=f'update {pipeline_type.value} pipeline {pipeline_name}',
                status=1, message='pipeline does not exist'))
        else:
            with open(pipeline_path) as pipeline_file:
                pipeline_contents = pipeline_file.read()
                pipeline_content_dict = json.loads(pipeline_contents)
                pipeline_content_dict.update(pipeline_content_updated)

            if pipeline_new_name:
                target_pipeline_name = pipeline_new_name
            else:
                target_pipeline_name = pipeline_name

            new_pipeline_path = f"ecoki/pipelines/custom_pipelines/{target_pipeline_name}"
            if check_pipeline_exists(new_pipeline_path):
                if not overwrite:
                    return PipelineContentResponse(
                        execution_status=ExecutionStatus(
                            command=f'update {pipeline_type.value} pipeline {pipeline_name}',
                            status=1, message='pipeline exists'))
            else:
                os.makedirs(new_pipeline_path)

            pipeline_json = json.dumps(pipeline_content_dict)
            with open(new_pipeline_path + "/settings.json", "w") as pipeline_file:
                pipeline_file.write(pipeline_json)
            return PipelineAddUpdateResponse(payload=PipelineAddUpdateInformation.parse_obj(pipeline_content_dict),
                                           execution_status=ExecutionStatus(
                                               command=f'update {pipeline_type.value} pipeline {pipeline_name}',
                                               status=0, message='OK'))

    async def delete_custom_pipeline(self, pipeline_name: str):
        # ---------------- delete custom pipelines --------------------
        try:
            shutil.rmtree(f"{self.pipeline_root_folder}/custom_pipelines/{pipeline_name}")
        except Exception as e:
            return DeletePipelineResponse(
                execution_status=ExecutionStatus(command=f'delete custom pipeline {pipeline_name}',
                                                 status=1,
                                                 message='failure when deleting a pipeline'))
        else:
            return DeletePipelineResponse(
                execution_status=ExecutionStatus(command=f'delete custom pipeline {pipeline_name}',
                                                 status=0,
                                                 message=f'pipeline {pipeline_name} has been deleted'))

    """async def filter_pipelines_by_keyword(self, pipeline_name: str, pipeline_type: PipelineTypes):
        # filter default pipelines
        filtered_pipelines = filter_pipelines(self.pipeline_root_folder, pipeline_type.name, pipeline_name)
        if filtered_pipelines:
            return FilterPipelineResponse(payload=filtered_pipelines, execution_status=ExecutionStatus(
                command=f'filter {pipeline_type.value} pipelines according to name/keyword {pipeline_name}',
                status=0,
                message='desired pipelines have been found'))

        else:
            return FilterPipelineResponse(
                execution_status=ExecutionStatus(
                    command=f'filter {pipeline_type.value} pipelines according to name/keyword {pipeline_name}',
                    status=1,
                    message='desired pipelines do not exist'))"""
