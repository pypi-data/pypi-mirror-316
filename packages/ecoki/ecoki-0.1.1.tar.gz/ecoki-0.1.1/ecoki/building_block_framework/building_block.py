from abc import ABC, abstractmethod

from ecoki.log_factory.local_log_handler import LocalLogHandler
from ecoki.common.base_classes import BuildingBlockDataStructure, BuildingBlockPortDataStructure
from ecoki.pipeline_framework.pipeline_manager.pipeline_manager import PipelineManager

class BuildingBlock(ABC, BuildingBlockDataStructure):
    """
        Base class of Building Block, inherits from data structure BuildingBlockDataStructure

        Attributes
        ----------
        name: str
            building block name
        description: str
            description of building block
        category: str
            category of building block
        version: str
            building block version
        architecture: str
            architecture of building block: ecoKI
        _inlet_ports: dict[str, BuildingBlockPortDataStructure]
            building block inlet ports list
        _outlet_ports: dict[str, BuildingBlockPortDataStructure]
            building block outlet ports list
        _settings: dict
            settings (building block configuration) of building block
        interactive_settings:bool
            True: activate interactive GUI
            False: deactivate interactive GUI, using static settings to configure BB
        pipeline_manager: str
            building block executor type: module path of building block local executor, default: "undefined"
        """
    def __init__(self, **kwargs):
        # kwrags: bb-related attributes of NodeInformation
        super().__init__(logger=LocalLogHandler(f'building block: {self.__class__.__name__}.{kwargs["name"]}.{id(self)}'), **kwargs)
        # use object id to distinguish loggers of the builing block with the same name,
        # otherwise the logs would be printed multiple time out

    def attach_pipeline_manager(self, pipeline_manager: PipelineManager):
        """
        register pipeline manager to building block
        :param pipeline_manager: pipeline manager object
        """
        self.pipeline_manager = pipeline_manager

    def set_settings(self, settings: dict):
        """
        set building block settings, called by building block executor
        :param settings: building block settings
        """
        self._settings = settings

    def _add_port(self, port_name: str, port_type, port_direction: str):
        """
        generic method, add inlet or outlet port to building block, called by methods add_inlet_port and add_outlet_port
        :param port_name: bb inlet port name
        :param port_type: data type of bb inlet port value
        :param port_direction: type of port: inlet or outlet
        """
        if self.check_port_exists(port_name, port_direction):
            self.logger.logger.error(f" Building block '{self.name}' {port_direction} port '{port_name}' already exist")

            return

        if port_direction == 'inlet':
            ports_list_var = self._inlet_ports
        elif port_direction == 'outlet':
            ports_list_var = self._outlet_ports
        else:
            raise KeyError(f" Direction {port_direction} is not allowed, only inlet or outlet are supported.")

        """ building block class uses the static bb port data structure. 
                Here we can use the same base class (BuildingBlockPortDataStructure) for static input and output"""
        ports_list_var[port_name] = BuildingBlockPortDataStructure(name=port_name, port_type=port_type,
                                                                   category=port_direction,
                                                                   data_type=port_type.__name__)

        self.logger.logger.info(f" Set {port_direction} port '{port_name}' to building block '{self.name}'")

    def add_inlet_port(self, port_name: str, port_type: type):
        """
        add inlet port to building block
        :param port_name: bb inlet port name
        :param port_type: data type of bb inlet port value
        """
        try:
            self._add_port(port_name, port_type, 'inlet')
        except Exception as e:
            self.logger.logger.error(e, exc_info=True)

    def add_outlet_port(self, port_name: str, port_type: type):
        """
        add outlet port to building block
        :param port_name: bb outlet port name
        :param port_type: data type of bb outlet port value
        """
        try:
            self._add_port(port_name, port_type, 'outlet')
        except Exception as e:
            self.logger.logger.error(e, exc_info=True)

    def check_port_exists(self, port_name: str, port_direction: str):
        """
        check whether the given building block port exist
        :param port_name: bb port name
        :param port_direction: inlet or outlet
        :return: True: bb port exists, False: bb doesn't exist
        """
        if port_direction == "inlet":
            return port_name in self._inlet_ports.keys()
        elif port_direction == "outlet":
            return port_name in self._outlet_ports.keys()
        else:
            raise KeyError(f" Direction {port_direction} is not allowed, only inlet or outlet are supported.")

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplementedError

    def get_inlets(self):
        """
        get building block inlet ports in dict
        :return: building block inlet ports in dictionary
        """
        return self._inlet_ports

    def get_outlets(self):
        """
        get building block outlet ports in dict
        :return: building block outlet ports in dictionary
        """
        return self._outlet_ports

    def get_port(self, port_name: str, port_direction: str):
        """
        get building block port obj according to given name and direction
        :param port_name: bb port name
        :param port_direction: inlet or outlet
        :return: building block port object
        """
        if not self.check_port_exists(port_name, port_direction=port_direction):
            raise KeyError(f" The given {port_direction} of port '{port_name}' doesn't exist")
        if port_direction == 'inlet':
            return self._inlet_ports[port_name]
        elif port_direction == 'outlet':
            return self._outlet_ports[port_name]
        else:
            return KeyError

    def reset_attributes(self):
        pass
