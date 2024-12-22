from abc import ABC, abstractmethod
from threading import Lock
from ecoki.log_factory.local_log_handler import LocalLogHandler
from ecoki.pipeline_framework.pipeline_executor.pipeline_executor import PipelineExecutor

class ThreadsManager(ABC):
    """
            Base class of thread manager

            Attributes
            ----------
            monitored_elements: dict
                dictionary containing to be executed pipeline threads
            logger: LocalLogHandler object
                local log handler obj used to record logs in log file and console
            """
    def __init__(self):
        self.monitored_elements = {}
        self.lock = Lock()
        self.logger = LocalLogHandler(f'Thread manager {__name__}.{self.__class__.__name__}.{id(self)}')

    @abstractmethod
    def add_thread(self, thread_name: str, element_executor: PipelineExecutor):
        raise NotImplementedError

    def thread_exists(self, thread_name: str):
        if thread_name in list(self.monitored_elements.keys()):
            return True
        else:
            return False

    @abstractmethod
    def remove_thread(self, thread_name: str):
        raise NotImplementedError

    def remove_all_threads(self):
        for thread_name in self.monitored_elements.keys():
            self.remove_thread(thread_name)

    @abstractmethod
    def run_thread(self, thread_name: str, inputs=None):
        raise NotImplementedError

    @abstractmethod
    def restart_thread(self, thread_name: str, execution_element: PipelineExecutor):
        raise NotImplementedError
