from ecoki.common.base_classes import ConnectionInformation


class Connection:
    """
        Connection class, connection is used to describe the relationship between nodes in a pipeline

        Attributes
        ----------
        name: str
            connection name
        from_node: str
            name of the incoming node (bb)
        from_port: str
            outlet port name of the incoming node (bb)
        to_node: str
            name of the target node (bb)
        to_port: str
            inlet port name of the the target node (bb)
    """
    def __init__(self, name, from_node, from_port, to_node, to_port):
        self.name = name
        self.from_node = from_node
        self.from_port = from_port
        self.to_node = to_node
        self.to_port = to_port
        
    def get_info_obj(self):
        """
        get connection information
        """
        return ConnectionInformation(name=self.name,
                                     from_node=self.from_node,
                                     from_port=self.from_port,
                                     to_node=self.to_node,
                                     to_port=self.to_port)
