import warnings
from ecoki.pipeline_framework.pipeline_executor.pipeline_executor import PipelineExecutor
from ecoki.building_block_framework.building_block_executor.local_building_block_executor import LocalBuildingBlockExecutor
from threading import Thread
from ecoki.pipeline_framework.topology_provider.topology_provider_from_dict import TopologyProviderFromDict
from ecoki.pipeline_framework.pipeline import Pipeline
from ecoki.pipeline_framework.pipeline_manager.pipeline_manager import PipelineManager
from ecoki.common.module_object_creator import create_executors, create_object_by_module
from ecoki.common.select_and_pass_arguments import pass_local_bb_executor_args
from ecoki.building_block_framework.building_block_executor.building_block_executor import BuildingBlockExecutor
import time
import os
import signal
from subprocess import Popen, PIPE


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def release_port(port):
    process = Popen(["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    for process in str(stdout.decode("utf-8")).split("\n")[1:]:
        data = [x for x in process.split(" ") if x != '']
        if (len(data) <= 1):
            continue

        os.kill(int(data[1]), signal.SIGKILL)


class LoopPipelineExecutor(PipelineExecutor):
    """
        class of LocalPipelineExecutor, inherits from the base class PipelineExecutor

        Attributes
        ----------
        pipeline: PipelineDataStructure
            pipeline object
        port_generator: PortNumberCounter
            generate port for bokeh server for visualization
        execution_sequence: list
            execution sequence of building blocks registered to the pipeline
        pipeline_execution: dict
            dictionary containing executors of building blocks registered to the pipeline
        execution_mode:
            execution_mode: int
            execution mode of pipeline: local
        _execution_status: int
            execution status of building block executor
            -1: wait to be execute
            0: is running
            1: execution is finished
        logger: LocalLogHandler
            local log handler obj used to record logs in log file and console
        host: int
            host(endpoint) of the backend server --remote access
    """
    def __init__(self, pipeline, **kwargs):
        super().__init__(pipeline, **kwargs)
        self._update_executors()
        self.loop_signal = True

    def _update_executors(self):
        """
        create/update bb executors in the pipeline
        step 1: find execution oder of bbs
        step 2: create bb executor for each bb registered in the pipeline and store it in dict pipeline_execution
        step 3: if needed, create visualizer for the bb and add it to the bb executor
        """
        self.pipeline_execution = {}
        self.logger.logger.info(" Creating executors")

        # new change: the building block executor is created according to the node information in pipeline topology
        for node in self.pipeline.topology.nodes:
            building_block = self.pipeline.nodes[node.name]
            self.logger.logger.info(f" Building block executor '{building_block.name}' created")

            bb_executor_args = pass_local_bb_executor_args(node)
            executor = create_executors(node.execution_mode, "building_block", building_block=building_block, **bb_executor_args)
            executor.set_settings(node.settings)

            self.pipeline_execution[node.name] = executor

            visualizer_module = node.visualizer_module
            input_name = node.visualizer_input

            if visualizer_module in ['undefined', '']:
                executor.visualizer = None
                continue
            try:
                visualizer_class_name = node.visualizer_class

                while True:
                    visualizer_port = self.port_generator.generate_port()
                    if is_port_in_use(visualizer_port):
                        self.port_generator.generated_ports.append(visualizer_port)
                    else:
                        break

                executor.visualizer = create_object_by_module(visualizer_module, visualizer_class_name,
                                                              visualizer_module=visualizer_module,
                                                              visualizer_class=visualizer_class_name,
                                                              endpoint=self.host,
                                                              port=visualizer_port,
                                                              input_name=input_name)

            except ModuleNotFoundError as exc:
                warnings.warn(
                    f'Visualizer of {building_block.name} of pipeline {self.pipeline.name} cannot be instantiated: {exc}')
                executor.visualizer = None

    def create_interactive_gui(self):
        """
        create interactive GUI objects and assign them to the corresponding building block
        executors. This method is related to the configure run pipeline button
        """
        for node in self.pipeline.topology.nodes:
            if node.interactive_configuration:
                executor = self.pipeline_execution[node.name]
                if executor.interactive_gui:
                    executor.interactive_gui.terminate()
                    interactive_gui_port = executor.interactive_gui.port
                else:
                    interactive_gui_port = self.port_generator.generate_port()  # assign port number to gui
                executor.building_block.interactive_settings = node.interactive_configuration
                building_block_path = node.building_block_module
                bb_path_list = building_block_path.split('.')
                bb_path_list[-1] = "interactive_gui"
                interactive_gui_path = '.'.join(bb_path_list)
                executor.interactive_configuration = True
                executor.interactive_gui_endpoint = f'{self.host}:{interactive_gui_port}'
                executor.interactive_gui = create_object_by_module(interactive_gui_path, "InteractiveGUI",
                                                                   endpoint=self.host,
                                                                   port=interactive_gui_port,
                                                                   building_block=executor.building_block)

    def deactivate_interactive_mode(self):
        """
        deactivate all interactive GUIs by setting interactive_configuration to false.
        This method is related to the run pipeline button
        """
        for node in self.pipeline.topology.nodes:
            if node.interactive_configuration:
                #node.interactive_configuration = False
                executor = self.pipeline_execution[node.name]
                executor.interactive_configuration = False
                #executor.interactive_gui = None
                executor.interactive_gui_endpoint = ''
                executor.building_block.interactive_settings = False
        self._terminate_bokeh_servers()

    def _run_executors(self):
        """
        run bb executors
        step 1: find inputs for the bb executor according to the connection info
        step 2: set input values to the corresponding bb executor
        step 3: run bb executor
        """
        self.logger.logger.info(" Run executors")
        for execution_element_name, execution_element in self.pipeline_execution.items():
            self.logger.logger.info(f" Executor {execution_element_name} is running")
            inputs = self._get_inputs_for_node(execution_element)
            execution_element.set_input_data(inputs)
            execution_element.run()
                
    def _terminate_bokeh_servers(self):
        """
        terminate server of the visualizer and interactive GUI
        """
        for execution_element_name, execution_element in self.pipeline_execution.items():
            if execution_element.interactive_gui:
                self.logger.logger.info(f" Terminating GUI {execution_element_name}")
                execution_element.interactive_gui.terminate()
                # release_port(execution_element.interactive_gui.port)
                self.logger.logger.info(f" GUI {execution_element_name} terminated")
                self.port_generator.free_port(execution_element.interactive_gui.port)

            if execution_element.visualizer:
                self.logger.logger.info(f" Terminating visualizer {execution_element_name}")
                execution_element.visualizer.terminate()
                # release_port(execution_element.visualizer.port)
                self.logger.logger.info(f" Visualizer {execution_element_name} terminated")
                self.port_generator.free_port(execution_element.visualizer.port)

    def _get_inputs_for_node(self, execution_node: BuildingBlockExecutor):
        """
        get inputs for the given node (bb) according to the connection info
        :param execution_node: building block executor
        :return: bb executor inputs dict --> {input_name: input_value}
        """
        node = execution_node.building_block
        incoming_connections = self.pipeline.get_incoming_connection_by_node(node)
        inputs_dict = {}
        for connection in incoming_connections:
            input_node = self.pipeline_execution[connection.from_node]
            input_value = input_node.outlet_ports_dict[connection.from_port].get_port_value()
            inputs_dict[connection.to_port] = input_value
        return inputs_dict

    def _run_routine(self):
        """
        steps needed to run a pipeline: step pipeline execution status, run bb executors, run visualizers
        """
        self.logger.logger.info(" Run pipeline")
        self.set_pipeline_execution_status(0)
        # self._update_executors()
        self._run_executors()
        self.set_pipeline_execution_status(1)

    def run(self):
        self.loop_signal = True
        """
        run pipeline executor
        """
        while self.loop_signal:
            self._run_routine()  # the method is going to be called in a separate pipeline thread
        
    def terminate(self):
        """
        terminate pipeline thread and the associated GUI and visualizer
        """
        self.logger.logger.info(f" Terminating pipeline thread for {self.pipeline.name}...")
        self.loop_signal = False
        self._terminate_bokeh_servers()

    def run_with_args(self, run_args: dict, pipeline_manager: PipelineManager):
        """
        run pipeline with additional arguments
        :param: run_args: additional arguments dictionary
        :param: pipeline manager, used to trigger another pipeline
        """
        orig_pipeline_executor = self
        orig_topology_dict = self.pipeline.topology_provider.provide()

        nodes_list = []
        connections_list = []
        # try:
        for input_data in run_args['inputs']:
            node_dict = {'name': input_data['building_block'] + '_' + input_data['inlet'],
                         'building_block_module': 'ecoki.building_blocks.code_based.static_value.static_value',
                         'building_block_class': 'StaticValue',
                         'settings': {'value': input_data['value']},
                         "execution_mode": 'local',
                         }
            nodes_list.append(node_dict)

            connection_dict = {'name': input_data['building_block'] + '_' + input_data['inlet'],
                               'from_node': input_data['building_block'] + '_' + input_data['inlet'],
                               'from_port': 'output_data',
                               'to_node': input_data['building_block'],
                               'to_port': input_data['inlet']}
            connections_list.append(connection_dict)

            if f'dedicated_execution_{nodes_list[0]["name"]}' in pipeline_manager.pipeline_thread_manager.monitored_elements.keys():
                pipeline_executor = pipeline_manager.pipeline_thread_manager.monitored_elements[
                    f'dedicated_execution_{nodes_list[0]["name"]}'].execution_element
                static_bb_executor = pipeline_executor.pipeline_execution[input_data['building_block'] + '_' + input_data['inlet']]
                static_bb_executor.set_settings({'value': input_data['value']})

        topology_dict = {'nodes': nodes_list + orig_topology_dict['nodes'],
                         'connections': connections_list + orig_topology_dict['connections']}
        topology_provider = TopologyProviderFromDict(topology_dict)
        # pipeline_manager = self.pipeline.pipeline_manager
        pipeline_manager = pipeline_manager

        if f'dedicated_execution_{nodes_list[0]["name"]}' in pipeline_manager.pipeline_thread_manager.monitored_elements.keys():
            pipeline_executor = pipeline_manager.pipeline_thread_manager.monitored_elements[
                f'dedicated_execution_{nodes_list[0]["name"]}'].execution_element
            pipeline = pipeline_executor.pipeline
        else:
            executor_module = orig_pipeline_executor.__module__
            executor_class = orig_pipeline_executor.__class__.__name__
            pipeline = Pipeline(name=f'dedicated_execution_{nodes_list[0]["name"]}', topology_provider=topology_provider,
                                pipeline_manager=pipeline_manager)
            pipeline_executor = create_object_by_module(executor_module, executor_class,
                                                        pipeline=pipeline, port_generator=self.port_generator)
        pipeline_manager.pipeline_thread_manager.add_thread(pipeline.name, pipeline_executor)
        pipeline_manager.pipeline_thread_manager.run_thread(pipeline.name)
        # pipeline_executor.run()
        # pipeline_executor.execution_thread.join()
        pipeline_manager.pipeline_thread_manager.monitored_elements[pipeline.name].join()
        output_values = []
        for output_data in run_args['outputs']:
            output_dict = {}
            output_dict['building_block'] = output_data['building_block']
            output_dict['outlet'] = output_data['outlet']
            executor = pipeline_executor.get_executor(output_data['building_block'])
            if executor:
                # output_dict['value'] = executor.building_block.get_port_value(output_data['outlet'], 'outlet')
                output_dict['value'] = executor.outlet_ports_dict[output_data['outlet']].get_port_value()
            output_values.append(output_dict)
        return output_values
        
        #except Exception as exc:
        #    self.logger.logger.warning(exc)
        #    return []
        