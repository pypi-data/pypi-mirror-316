from datetime import datetime
from ecoki.building_block_framework.building_block_executor.building_block_executor import BuildingBlockExecutor
from ecoki.common.status_code import Status

class LocalBuildingBlockExecutor(BuildingBlockExecutor):
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
        super().__init__(building_block, **kwargs)

    def run(self):
        """
        new change: the run method of bb executor contains 3 steps:
        1. run interactive gui (if needed)
        2. run building block
        3. pass results to visualizer and run visualizer
        """
        inputs_dict = {}
        """
        the building block method execute now accepts a dict containing the inputs. 
        First in the run method of bb executor, the input values will be extracted for bb executor input ports,
        then a input dict (inputs_dict) will be created and passed to the bb execute method
        """
        self.set_bb_execution_status(Status.RUNNING.value)  # status 0: bb is ready to be executed
        # ---------------------interactive gui ----------------------------
        if self.interactive_configuration:  # if true, building block executor will activate interactive mode
            try:
                for input_name in self.interactive_gui.inputs_name:   # assign results to gui, if it requires some inputs (dependents on the results of previous bb)
                    self.interactive_gui.inputs[input_name] = self.inlet_ports_dict[input_name].get_port_value()
                bb_settings = self.interactive_gui.run_interactive_gui()  # run interactive gui
                self.set_settings(bb_settings)
            except Exception as exc:
                self.logger.logger.error(f'Cannot execute gui of building block {self.building_block.name}')
                self.logger.logger.error(exc, exc_info=True)

        # ---------------------building block execution ----------------------------
        for input_name, inlet_port in self.inlet_ports_dict.items():  # create inputs dict for bb execution
            inputs_dict[input_name] = inlet_port.get_port_value()

        self.execution_start = datetime.now()  # toDO: execution time just for benchmarking?

        try:
            execution_results = self.building_block.execute(**inputs_dict)  # new change: bb execute method accepts now a dict
            """
            set bb results to the corresponding outlet ports of bb executor
            """
            if execution_results:
                for name, value in execution_results.items():
                    self.set_output_data(name, value)
                    self.logger.logger.info(f" Output of building block '{self.building_block.name}' in port '{name}': {value}")

        except Exception as exc:
            self.set_bb_execution_status(Status.FAILURE.value)
            self.logger.logger.error(f'Cannot execute building block {self.building_block.name}')
            self.logger.logger.error(exc, exc_info=True)

        else:
            self.set_bb_execution_status(Status.FINISHED.value)
            self.execution_end = datetime.now()  # toDO: execution time just for benchmarking?
            self.execution_time = (self.execution_end - self.execution_start).total_seconds()
            # self.validate_results()

        # ---------------------visualizer ----------------------------
        if self.visualizer:
            try:
                if type(self.visualizer.input_name) == dict:
                    for key, value in self.visualizer.input_name.items():
                        self.visualizer.input_dict[key] = self.outlet_ports_dict[value].get_port_value()
                else:
                    for i in self.visualizer.input_name:
                        self.visualizer.input_dict[i] = self.outlet_ports_dict[i].get_port_value()
                self.visualizer.run()

            except Exception as exc:
                self.logger.logger.error(f'Cannot execute visualizer of building block {self.building_block.name}')
                self.logger.logger.error(exc, exc_info=True)

    # toDO: validate results
    def validate_results(self):
        pass
