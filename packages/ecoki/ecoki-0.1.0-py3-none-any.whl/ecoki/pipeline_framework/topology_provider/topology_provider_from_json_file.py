from ecoki.pipeline_framework.topology_provider.topology_provider import TopologyProvider
import json


class TopologyProviderFromJSONFile(TopologyProvider):
    """
       class TopologyProviderFromJSONFile, inherits from the base class TopologyProvider, used in LocalPipelineExecutor to provide topology from a JSON file

       Attributes
       ----------
       path_to_file: str
           path of the JSON file
       topology: dict
           topology in dict parsed from the given JSON file
       """
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.topology = {}
        self._read_from_file()

    def _read_from_file(self):
        """
        read JSON file and parse it to topology dict
        """
        with open(self.path_to_file) as f:
            self.topology = json.load(f)

    def provide(self):
        """
        return topology in dictionary
        """
        return self.topology["topology"]
