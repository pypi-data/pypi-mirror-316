from abc import ABC, abstractmethod


class Shell(ABC):
    @abstractmethod
    def run(self):
        pass