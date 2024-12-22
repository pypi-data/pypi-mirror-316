from abc import ABC, abstractmethod
from threading import Thread

from ecoki.log_factory.local_log_handler import LocalLogHandler
from ecoki.common.base_classes import PipelineInformationWithPorts, PipelineTopologyInformationWithPorts, NodeInformation, PipelineTopologyInformation, ConnectionInformation, PipelineExecutorDataStructure, PipelineInformation


class PipelineExecutor(ABC, PipelineExecutorDataStructure):
    """
        Base class of pipeline executor, inherits from data structure PipelineExecutorDataStructure

        Attributes
        ----------
        pipeline: PipelineDataStructure
            pipeline object
        port_generator: PortNumberCounter
            generate port for bokeh server for visualization
        execution_sequence: list
            execution sequence of building blocks registered to the pipeline
        pipeline_execution: dict
            dictionary containing executors of building blocks registered to the pipeline
        execution_mode:
            execution_mode: int
            execution mode of pipeline: local
        _execution_status: int
            execution status of building block executor
            -1: wait to be execute
            0: is running
            1: execution is finished
        logger: LocalLogHandler
            local log handler obj used to record logs in log file and console
        host: int
            host(endpoint) of the backend server --remote access
    """
    def __init__(self, pipeline, **kwargs):
        super().__init__(pipeline=pipeline, logger=LocalLogHandler(f'local pipeline executor: {pipeline.name}.{id(self)}'), **kwargs)


    def _find_execution_order(self):
        # toDO: if the order of BBs specified in connection.json does not comply with the execution order,
        #  we should sort BBs according to their internal inputs
        self.execution_sequence = [item for _, item in self.pipeline.nodes.items()]  # toDO

    # toDO: maintain the BB threads within pipeline
    def handle_bb_threads(self):
        pass
    
    @abstractmethod
    def _update_executors(self):
        """
       create/update bb executors in the pipeline, implemented in the subclass LocalPipelineExecutor
       """
        raise NotImplementedError

    @abstractmethod
    def _run_executors(self):
        """
        run pipeline executor, implemented in the subclass LocalPipelineExecutor
        """
        raise NotImplementedError

    @abstractmethod
    def _get_inputs_for_node(self, node):
        """
        get inputs for the given node (bb), implemented in the subclass LocalPipelineExecutor
        :param node: building block executor
        """
        raise NotImplementedError

    @abstractmethod
    def _run_routine(self):
        """
        separate pipeline execution into several steps, implemented in the subclass LocalPipelineExecutor
        """
        raise NotImplementedError

    @abstractmethod
    def run(self):
        # overwritten by subclass LocalPipelineExecutor
        raise NotImplementedError
    
    @abstractmethod
    def terminate(self):
        raise NotImplementedError
        
    def get_topology_info_obj(self):
        """
        get pipeline topology info for RESTApi, nodes: bb executor objects, connections: connection info
        :return: basic data structure PipelineInformation
        """
        nodes = [node_executor.get_info_obj_for_topology() for node_executor in self.pipeline_execution.values()]
        connections = [connection.get_info_obj() for connection in self.pipeline.connections.values()]
        return PipelineInformation (name=self.pipeline.name,
                                    #description=self.pipeline.description,
                                    #version=self.pipeline.version,
                                    topology=PipelineTopologyInformation(nodes=nodes, connections=connections),
                                    execution_mode=self.execution_mode,
                                    execution_status=self.get_pipeline_execution_status(),
                                    metadata=self.pipeline.metadata
                                    )    

    def get_info_obj(self):
        """
        get basic pipeline info containing pipeline name, description, version and topology info
        :return: basic data structure PipelineInformationWithPorts
        """
        nodes = [node_executor.get_info_obj() for node_executor in self.pipeline_execution.values()]
        connections = [connection.get_info_obj() for connection in self.pipeline.connections.values()]
        topology = PipelineTopologyInformationWithPorts(nodes=nodes,
                                                        connections=connections)
        return PipelineInformationWithPorts(name=self.pipeline.name,
                                            #description=self.pipeline.description,
                                            #version=self.pipeline.version,
                                            topology=topology,
                                            execution_mode=self.execution_mode,
                                            execution_status=self.get_pipeline_execution_status(),
                                            metadata=self.pipeline.metadata)
        
    def executor_exists(self, node_name):
        """
        check whether bb executor exists in the pipeline according to the given bb name
        :param node_name: bb name
        :return: True: bb executor exists, False: bb executor doesn't exist
        """
        if node_name in self.pipeline_execution:
            return True
        else:
            return False
        
    def get_executor(self, node_name: str):
        """
        get bb executor according to the given bb name
        :param node_name: bb name
        :return: building block executor object, if not exist: None
        """
        if self.executor_exists(node_name):
            return self.pipeline_execution[node_name]
        else:
            return None

    def add_node(self, node: NodeInformation, pos=-1):
        """
        add bb executor to the current pipeline according to the given node info and update pipeline
        :param node: node (bb) information
        :return: if the desired bb executor is added to the pipeline successfully: True, otherwise: False
        """
        add_node_status = self.pipeline.add_node(node)
        if add_node_status:
            self._update_executors()
        return add_node_status

    def delete_node(self, node_name:str):
        """
        delete bb executor from the current pipeline according to the given bb executor name and update pipeline
        :param node_name: name of bb executor to be removed
        :return: if the desired bb executor is removed from the pipeline successfully: True, otherwise: False
        """
        delete_node_status = self.pipeline.delete_node(node_name)
        if delete_node_status:
            self._update_executors()
        return delete_node_status

    def add_connection(self, connection: ConnectionInformation, pos=-1):
        """
        add new connection to the current pipeline according to the given connection info and update pipeline
        :param connection: connection information
        :return: if the connection is added to the pipeline successfully: True, otherwise: False
        """
        add_connection_status = self.pipeline.add_connection(connection)
        if add_connection_status:
            self._update_executors()
        return add_connection_status

    def delete_connection(self, connection_name:str):
        """
        delete connection from the current pipeline according to the given connection name and update pipeline
        :param connection_name: name of connection to be removed
        :return: if the connection is removed from the pipeline successfully: True, otherwise: False
        """
        delete_connection_status = self.pipeline.delete_connection(connection_name)
        if delete_connection_status:
            self._update_executors()
        return delete_connection_status

    def set_pipeline_execution_status(self, status_code: int):
        self._execution_status = status_code

    def get_pipeline_execution_status(self):
        return self.execution_status
