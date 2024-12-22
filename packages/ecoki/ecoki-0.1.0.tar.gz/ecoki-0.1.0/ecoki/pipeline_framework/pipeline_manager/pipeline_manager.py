from ecoki.pipeline_framework.pipeline_executor.pipeline_executor import PipelineExecutor
from ecoki.pipeline_framework.pipeline import Pipeline
from ecoki.pipeline_framework.topology_provider.topology_provider import TopologyProvider
from ecoki.pipeline_framework.pipeline_manager.port_number_counter import PortNumberCounter
from ecoki.common.module_object_creator import create_executors
from ecoki.threads_management.threads_manager.pipeline_thread_manager import PipelineThreadManager


class PipelineManager:
    """
        class PipelineManager that is responsible for the pipeline management (getting/checking/adding/removing pipelines)

        Attributes
        ----------
        pipelines: {}
            dict containing pipeline executors of the active pipelines
        port_generator: PortNumberCounter
            bokeh server port generator
        host: str:
            host of the pipeline manager (the same as the backend)
        pipeline_thread_manager: object:
            pipeline thread manager object used to start/restart/pipeline in a separate thread
    """
    def __init__(self, port_generator, host="127.0.0.1"):
        self.pipelines = {}
        self.port_generator = port_generator
        self.host = host
        self.pipeline_thread_manager = PipelineThreadManager()

    def get_pipeline(self, pipeline_name:str):
        """
        get a pipeline according to the give pipeline name
        :param pipeline_name: pipeline name
        """
        if self.pipeline_exists(pipeline_name):
            return self.pipelines[pipeline_name].pipeline
        return None

    def get_pipeline_executor(self, pipeline_name:str):
        """
        get a pipeline executor according to the give pipeline name
        :param pipeline_name: pipeline name
        """
        if self.pipeline_exists(pipeline_name):
            return self.pipelines[pipeline_name]
        return None

    def pipeline_exists(self, pipeline_name:str):
        """
        check the existence of a pipeline according to the give pipeline name
        :param pipeline_name: pipeline name
        :return: if pipeline exists: True, otherwise: False
        """
        return pipeline_name in self.pipelines.keys()

    def add_pipeline(self, pipeline_name: str, pipeline_execution_mode: str, topology_provider:TopologyProvider, metadata):
        """
        add a new pipeline to the system
        :param pipeline_name: pipeline name
        :param topology_provider: topology provider of the pipeline
        :param pipeline_execution_mode: execution mode of pipeline: local
        """
        if self.pipeline_exists(pipeline_name):
            return False
        pipeline = Pipeline(name=pipeline_name, topology_provider=topology_provider, pipeline_manager=self, metadata=metadata)

        pipeline_executor = create_executors(pipeline_execution_mode, "pipeline",
                                             pipeline=pipeline, port_generator=self.port_generator, host=self.host)
        self.pipelines[pipeline_name] = pipeline_executor
        self.pipeline_thread_manager.add_thread(pipeline_name, pipeline_executor)
        return True

    def delete_pipeline(self, pipeline_name:str):
        """
        delete a pipeline and its executor according to the given pipeline name
        :param pipeline_name: pipeline name
        """
        if self.pipeline_exists(pipeline_name):
            self.pipelines.pop(pipeline_name)
            self.pipeline_thread_manager.remove_thread(pipeline_name)
            return True
        else:
            return False

    def get_info_obj(self):
        """
        get the information of all active pipelines and their executors
        """
        return [pipeline_exec.get_info_obj() for pipeline_exec in self.pipelines.values()]
