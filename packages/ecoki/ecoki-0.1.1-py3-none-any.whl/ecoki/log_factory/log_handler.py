from enum import Enum
from abc import ABC, abstractmethod
import logging


class LoggingLevel(Enum):
    """
    define different log level for log handler
    """
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LogHandler(ABC):
    """
        Base class of log handler

        Attributes
        ----------
        _name : str
            log handler name
        logger : logger object of module logging
            building block port category: inlet or outlet
        """
    def __init__(self, name):
        self._name = name
        self.logger = logging.getLogger(self._name)
        self.logger.setLevel(LoggingLevel["DEBUG"].value)

    def add_handler_to_logger(self, handler):
        """
        add the given handler (file handler, stream handler) to logger
        """
        self.logger.addHandler(handler)
