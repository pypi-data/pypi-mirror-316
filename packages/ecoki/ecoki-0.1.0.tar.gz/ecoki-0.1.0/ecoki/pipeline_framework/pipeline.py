import warnings
from ecoki.pipeline_framework.connection import Connection
from ecoki.common.base_classes import NodeInformation, ConnectionInformation, PipelineTopologyInformation, PipelineDataStructure, TBB
from ecoki.common.module_object_creator import create_object_by_module
from ecoki.common.select_and_pass_arguments import pass_building_block_args

class Pipeline(PipelineDataStructure):
    """
        Base class of pipeline, inherits from data structure PipelineDataStructure

        Attributes
        ----------
        topology: PipelineTopologyInformation
            pipeline topology object --> nodes: [], connections: []
        nodes: dict
            nodes (building blocks) dictionary containing building block
         connections: dict
            connections dictionary containing connection objects
        name: str
            pipeline name
        description: str:
            pipeline description
        version: str:
            pipeline version
        topology_provider: object
            topology provider object: for RESTAPI: TopologyProviderFromJSON, for local execution: TopologyProviderFromJSONFile
        pipeline_manager: object
            pipeline_manager object
        execution_mode: int
            execution mode of pipeline: local

    """
    def __init__(self, name, metadata, topology_provider=None, description='', version='', pipeline_manager=None):
        super().__init__(name=name, description=description,  version=version, topology_provider=topology_provider, pipeline_manager=pipeline_manager, meatadata=metadata)
        self.topology = PipelineTopologyInformation()
        self.metadata = metadata
        self.create_pipeline()

    def node_exists(self, node_name: str):
        """
        check the existence of a building block according to the given name
        :param node_name: node (bb) name
        :return: True: desired node (bb) exists, False: desired node (bb) doesn't exist
        """
        if node_name in self.nodes:
            return True
        else:
            return False

    def add_node(self, node: NodeInformation, pos=None):
        """
        add building block to the pipeline topology according to the given node (bb) information
        :param node: NodeInformation object
        :param pos: position of the added building block, default: the last position
        """
        if not pos:
            self.topology.nodes.insert(len(self.topology.nodes), node)  # !!! list.insert(-1, element) doesn't work !!!
        else:
            self.topology.nodes.insert(pos, node)
        bb_module_path = node.building_block_module
        bb_class_name = node.building_block_class

        try:
            bb_args = pass_building_block_args(node)
            bb = create_object_by_module(bb_module_path, bb_class_name, **bb_args)
            bb.attach_pipeline_manager(self.pipeline_manager)
        except ModuleNotFoundError as exc:
            warnings.warn(f'Cannot add node {node.name} to the pipeline {self.name}: {exc}')
            return False

        self.nodes[node.name] = bb
        return True

    def delete_node(self, node_name:str):
        """
        delete a node (bb) from pipeline according to the given bb name
        :param node_name: node (bb) name
        """
        if not self.node_exists(node_name):
            return False
        self.nodes.pop(node_name)
        for node in self.topology.nodes:
            if node.name==node_name:
                self.topology.nodes.remove(node)
                return True
        return False        

    def get_node(self, node_name:str):
        """
        get node (bb) object according to the given name
        :param node_name: node (bb) name
        """
        if not self.node_exists(node_name):
            return False
        return self.nodes[node_name]

    def connection_exists(self, connection_name:str):
        """
       check the existence of the connection according to the connection name
       :param connection_name: connection name
       :return: True: desired connection exists, False: desired connection doesn't exist
       """
        if connection_name in self.connections.keys():
            return True
        else:
            return False

    def add_connection(self, connection: ConnectionInformation, pos=-1):
        """
        add new connection to the pipelien topology according to the connection info
        :param connection: ConnectionInformation object
        :param pos: position of the new added connection, default: -1
        """

        self.topology.connections.insert(pos, connection)
        self.connections[connection.name] = Connection(name=connection.name,
                                                        from_node=connection.from_node,
                                                        from_port=connection.from_port,
                                                        to_node=connection.to_node,
                                                        to_port=connection.to_port)
        return True

    def delete_connection(self, connection_name:str):
        """
        delete a connection from pipeline according to the given connection name
        :param connection_name: connection name
        """
        if not self.connection_exists(connection_name):
            return False
        self.connections.pop(connection_name)
        return True

    def get_connection(self, connection_name:str):
        """
        get connection obj according to the given name
        :param connection_name: connection name
        """
        if not self.connection_exists(connection_name):
            return None
        return self.connections[connection_name]

    def get_incoming_connection_by_node(self, node: TBB):
        """
        search the incoming connections for each node (bb) according to the connections attribute in pipeline topology
        :param node: node (bb) object
        :return: incoming connection list
        """
        incoming_connection = []
        for connection in self.connections.values():
            if connection.to_node == node.name:
                incoming_connection.append(connection)
        return incoming_connection

    def create_pipeline(self):
        """
        create topology (nodes and connections) for  by calling self.add_node and self.add_connection
        """
        if self.topology_provider is None:
            return

        topology = self.topology_provider.provide()

        for node in topology["nodes"]:
            node_obj = NodeInformation.parse_obj(node)
            self.add_node(node_obj)

        for connection in topology["connections"]:
            connection_obj = ConnectionInformation.parse_obj(connection)
            self.add_connection(connection_obj)

    def attach_topology_provider(self, topology_provider):
        self.topology_provider = topology_provider
        self.create_pipeline()