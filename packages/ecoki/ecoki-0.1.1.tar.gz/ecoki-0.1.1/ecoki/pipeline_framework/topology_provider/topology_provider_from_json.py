from ecoki.pipeline_framework.topology_provider.topology_provider import TopologyProvider
import json


class TopologyProviderFromJSON(TopologyProvider):
    """
      class TopologyProviderFromJSON, inherits from the base class TopologyProvider, used to in RESTAPI provide topology in JSON format

      Attributes
      ----------
      topology: str
          topology in JSON
       """
    def __init__(self, json_data):
        self.topology = json_data
        
    def provide(self):
        """
        return topology in dictionary
        """
        return self.topology.dict()