from ecoki.log_factory.log_handler import LogHandler, LoggingLevel
import logging


class LoggerNameFilter(logging.Filter):
    def filter(self, record):
        name_list = record.name.split('.')
        name_list.pop(-1)
        record.log_title = '.'.join(name_list)
        return True


class LocalLogHandler(LogHandler):
    """
        local log handler class, used to record log, error, warning and so on into the central log file and console

        Attributes
        ----------
        _name : str
            log handler name
        logger :
            logger object of module logging
        console_level: str
            log level of stream handler: DEBUG by default
        file_path: str
            location of the central log file
        file_level: str
            log level of file handler: DEBUG by default
        """
    def __init__(self, name, console_level="DEBUG", file_path="debug.log", file_level="DEBUG"):
        super().__init__(name)
        self._set_console_handler(LoggingLevel[console_level].value, '[%(asctime)s] %(levelname)s: [%(log_title)s]:%(message)s')
        self._set_file_handler(file_path, LoggingLevel[file_level].value, '[%(asctime)s] %(levelname)s: [%(log_title)s]:%(message)s')

    def _set_console_handler(self, log_level, log_format):
        """
        configure stream handler
        :param log_level: log level of stream handler: DEBUG by default
        :param log_format: log format of stream handler
        """
        console_handler = logging.StreamHandler()
        console_handler_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_handler_formatter)
        console_handler.setLevel(log_level)
        console_handler.addFilter(LoggerNameFilter())
        self.add_handler_to_logger(console_handler)

    def _set_file_handler(self, file_path, log_level, log_format):
        """
        configure file handler
        :param log_level: log level of file handler: DEBUG by default
        :param log_format: log format of file handler
        """
        file_handler = logging.FileHandler(file_path, mode='a')
        file_handler_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_handler_formatter)
        file_handler.setLevel(log_level)
        file_handler.addFilter(LoggerNameFilter())
        self.add_handler_to_logger(file_handler)
