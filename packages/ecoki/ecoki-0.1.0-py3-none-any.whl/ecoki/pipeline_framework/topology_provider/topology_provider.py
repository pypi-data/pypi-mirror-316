from abc import ABC, abstractmethod


class TopologyProvider(ABC):
    """
    Base class of topology provider, used to create topology (nodes, connections) for pipeline
    """
    @abstractmethod
    def provide(self):
        pass
