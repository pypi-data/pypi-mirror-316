from ecoki.pipeline_framework.topology_provider.topology_provider import TopologyProvider


class TopologyProviderFromDict(TopologyProvider):
    """
        class TopologyProviderFromDict, inherits from the base class TopologyProvider, used to parse the dictionary topology

        Attributes
        ----------
        topology: dict
            dictionary topology
        """
    def __init__(self, topology_dict):
        self.topology = topology_dict
        
    def provide(self):
        return self.topology