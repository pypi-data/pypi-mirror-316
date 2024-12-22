from abc import ABC, abstractmethod
from ecoki.log_factory.local_log_handler import LocalLogHandler
from ecoki.common.base_classes import BuildingBlockInformationWithPorts, BuildingBlockInformationWithValues, NodeInformation, BuildingBlockExecutorDataStructure
from ecoki.building_block_framework.building_block_port.building_block_port_inlet import BuildingBlockPortInlet
from ecoki.building_block_framework.building_block_port.building_block_port_outlet import BuildingBlockPortOutlet


class BuildingBlockExecutor(ABC, BuildingBlockExecutorDataStructure):
    """
        Base class of Building Block executor, inherits from data structure BuildingBlockExecutorDataStructure

        Attributes
        ----------
        building block: BuildingBlock
            building block to be executed
        visualizer: object
            building block visualizer obj (if needed)
        interactive_gui: object
            interactive GUI object (if interactive_configuration is set to True)
        execution_mode: str
            execution mode of building block: local
        bb_status: int
            status of building block
        _execution_status: int
            execution status of building block executor
            -1: wait to be execute
            0: is running
            1: execution is finished
        execution_start: datetime
            execution start time of BB executor
        execution_end: datetime
            execution end time of BB executor
        execution_time: float
            execution time of building block
        inlet_ports_dict: dict
            input ports dictionary of BB executor (Ports of executor contain values)
        outlet_ports_dict: dict
            output ports dictionary of BB executor (Ports of executor contain values)
        logger: LocalLogHandler object
            local log handler obj used to record logs in log file and console
        interactive_configuration: bool
            True: activate interactive GUI
            False: deactivate interactive GUI, using static settings to configure BB
        interactive_gui_endpoint: str
            endpoint of interactive GUI server
        visualization_endpoint: str
            endpoint of visualizer server
        visualizer_module: str
            module path of visualizer class
        visualizer_class: str
            name of visualizer class
        settings: dict
            settings (building block configuration) of building block
        """
    def __init__(self, building_block, **kwargs):
        # kwrags: bb executor-related attributes of NodeInformation
        super().__init__(building_block=building_block, logger=LocalLogHandler(f'local building block executor: {building_block.name}.{id(self)}'), **kwargs)
        self._create_ports()

    def _create_ports(self):
        """
        according to the static bb ports, creat input and output ports (bb port with values) for bb executor
        building_block.inlet_ports: static bb ports (without values)
        BuildingBlockPortInlet: dynamic bb executor ports (with values)
        """
        for key, value in self.building_block.get_inlets().items():
            self.inlet_ports_dict[key] = BuildingBlockPortInlet.parse_obj(value.dict())

        for key, value in self.building_block.get_outlets().items():
            self.outlet_ports_dict[key] = BuildingBlockPortOutlet.parse_obj(value.dict())

    def set_settings(self, settings: dict):
        """
        :param settings: building block settings
        set settings for building block. Here we do it in bb executor not in bb anymore
        """
        self.building_block.set_settings(settings)

    def set_input_data(self, inputs: dict):
        """
        :param: inputs: inputs dict
        set input values from a dict to the corresponding input ports
        """
        for name, value in inputs.items():
            self.inlet_ports_dict[name].set_port_value(value)

    def set_output_data(self, name: str, value):
        """
        set the bb results to the output ports of bb executor.
        --> with the help of bb executor ports we can enable standard access to the bb results
        :param: name: name of output port
        :param: value: value of output port
        """
        self.outlet_ports_dict[name].set_port_value(value)
        self.outlet_ports_dict[name].set_status_code(0)

    @abstractmethod
    def run(self):
        """
        run building block, implemented in the subclass LocalBuildingBlockExecutor
        """
        raise NotImplementedError

    def set_bb_status(self):
        # TODO set building block status, to be implemented in second release version
        pass

    def get_bb_status(self):
        """
        get building block status
        :return: bb_status
        """
        return self.bb_status

    def set_bb_execution_status(self, status_code: int):
        """
        set the execution status of BB
        :param status_code: BB execution status
            -1: wait to be execute
            0: is running
            1: execution is finished
        """
        self._execution_status = status_code

    def get_bb_execution_status(self):  # True, running, (future: running, waiting, stoped)
        """
        get building block status
        :return: bb executor status --> waiting, running, failure and finished
        """
        return self.execution_status

    def stop_bb(self):
        # TODO: to be implemented in second release version
        pass

    def restart_bb(self):
        # TODO: to be implemented in second release version
        pass

    def combine_ports(self):
        """
        get bb inlet and outlet ports combined in a single dict
        """
        return {**self.inlet_ports_dict, **self.outlet_ports_dict}

    def get_info_obj_for_topology(self):
        """
        get building block basic information
        :return: data structure NodeInformation
        """
        return NodeInformation(name=self.building_block.name,
                               building_block_module=self.building_block.__module__,
                               building_block_class=self.building_block.__class__.__name__,
                               execution_mode=self.execution_mode,
                               settings=self.building_block.settings,
                               visualizer_module=self.visualizer.visualizer_module if self.visualizer is not None else '',
                               visualizer_class=self.visualizer.visualizer_class if self.visualizer is not None else '',
                               visualizer_input=self.visualizer.input_name if self.visualizer is not None else [],
                               )

    def get_info_obj(self):
        """
        get building block information and basic bb port information
        :return: data structure BuildingBlockInformationWithPorts
        """
        return BuildingBlockInformationWithPorts(name=self.building_block.name,
                                                 description=self.building_block.description,
                                                 category=self.building_block.category,
                                                 building_block_module=self.building_block.__module__,
                                                 building_block_class=self.building_block.__class__.__name__,
                                                 settings=self.building_block.settings,
                                                 execution_mode=self.execution_mode,
                                                 ports=[port.get_info_obj() for port in
                                                        self.combine_ports().values()],
                                                 visualizer_module=self.visualizer_module,
                                                 visualizer_class=self.visualizer_class,
                                                 visualization_endpoint=f'{self.visualizer.endpoint}:{self.visualizer.port}' if self.visualizer is not None else '',
                                                 visualizer_input=self.visualizer.input_name if self.visualizer is not None else [],
                                                 interactive_configuration=self.interactive_configuration,
                                                 interactive_gui_endpoint=self.interactive_gui_endpoint,
                                                 execution_status=self.get_bb_execution_status()
                                                 )

    def get_info_obj_with_values(self):
        """
        get building block information and bb port information with bb values
        :return: data structure BuildingBlockInformationWithValues
        """
        return BuildingBlockInformationWithValues(name=self.building_block.name,
                                                  description=self.building_block.description,
                                                  category=self.building_block.category,
                                                  building_block_module=self.building_block.__module__,
                                                  building_block_class=self.building_block.__class__.__name__,
                                                  settings=self.building_block.settings,
                                                  execution_mode=self.execution_mode,
                                                  ports=[port.get_info_obj_with_values() for port in
                                                         self.combine_ports().values()],
                                                  visualizer_module=self.visualizer_module,
                                                  visualizer_class=self.visualizer_class,
                                                  visualization_endpoint=f'{self.visualizer.endpoint}:{self.visualizer.port}' if self.visualizer is not None else '',
                                                  visualizer_input=self.visualizer.input_name if self.visualizer is not None else [],
                                                  interactive_configuration=self.interactive_configuration,
                                                  interactive_gui_endpoint=self.interactive_gui_endpoint,
                                                  execution_status=self.get_bb_execution_status()

                                                  )

