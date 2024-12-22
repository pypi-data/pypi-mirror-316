from enum import Enum
from pydantic import BaseModel, Field, validator, ValidationError, PrivateAttr
from typing import Any, TypeVar, Union
from datetime import datetime
from threading import Thread
from ecoki.log_factory.local_log_handler import LocalLogHandler
from ecoki.visualizer_framework.visualizer import Visualizer
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
from ecoki.pipeline_framework.topology_provider.topology_provider import TopologyProvider
from ecoki.pipeline_framework.pipeline_manager.port_number_counter import PortNumberCounter


# --------------  pydantic data models for RestAPI responses ----------------
class PortCategory(str, Enum):
    inlet = "inlet"
    outlet = "outlet"

class PortInformation(BaseModel):
    name: str = ''
    category: str = ''
    data_type: str = ''
    allowed_data_types: list = []

class PortInformationWithValues(PortInformation):
    values: object = None

class ConnectionInformation(BaseModel):
    name: str = ''
    from_node: str = ''
    from_port: str = ''
    to_node: str = ''
    to_port: str = ''

class NodeInformation(BaseModel):  # nodeinfo class is used to store each bb entry of the settings.json
    name: str = ''
    building_block_module: str = 'undefined'
    building_block_class: str = 'undefined'
    execution_mode: str = 'undefined'  # currently the only execution mode is local, with the use of this flag we can replace the module path and class name of bb executor
    settings: dict = {}
    visualizer_module: str = 'undefined'
    visualizer_class: str = 'undefined'
    interactive_configuration: bool = False

    """ new change: this list contains the name of bb results that have to be visualized, 
        so that we can separate bb and visualizer (we don't have to assign bb obj to visualizer)"""
    visualizer_input: Union[dict, list] = {}


class BuildingBlockInformation(NodeInformation):
    description: str = ''
    category: str = 'undefined'
    visualization_endpoint: str = ''
    interactive_gui_endpoint: str = ''
    execution_status: int = -1

class BuildingBlockInformationWithPorts(BuildingBlockInformation):
    ports: list[PortInformation] = []

class BuildingBlockInformationWithValues(BuildingBlockInformation):
    ports: list[PortInformationWithValues] = []

class PipelineTopologyInformation(BaseModel):
    nodes: list[NodeInformation] = []
    connections: list[ConnectionInformation] = []

class PipelineTopologyInformationWithPorts(BaseModel):
    nodes: list[BuildingBlockInformationWithPorts] = []
    connections: list[ConnectionInformation] = []

class PipelineTopologyInformationWithValues(BaseModel):
    nodes: list[BuildingBlockInformationWithPorts] = []
    connections: list[ConnectionInformation] = []

class PipelineInformation(BaseModel):
    name: str = ''
    topology: PipelineTopologyInformation = PipelineTopologyInformation()
    execution_mode: str = 'undefined'  # use execution mode to replace module path and class name of pipeline executor
    execution_status: int = -1
    metadata: dict = {}

class PipelineInformationWithPorts(PipelineInformation):
    topology: PipelineTopologyInformationWithPorts = PipelineTopologyInformationWithPorts()

class PipelineInformationWithValues(PipelineInformation):
    topology: PipelineTopologyInformationWithValues = PipelineTopologyInformationWithValues()

class PipelineManagerInformation(BaseModel):
    pipelines: list[PipelineInformationWithPorts] = []

class ExecutionStatus(BaseModel):
    command: str = 'undefined'
    status: int = -1
    message: str = 'undefined'


# --------------  pydantic data models for basic ecoKI classes ----------------
class BuildingBlockPortDataStructure(PortInformation):
    """basic building block class, a static data structure. It doesn't contain any value and is assigned to bb class"""
    port_type: type


class BuildingBlockPortWithValues(BuildingBlockPortDataStructure):
    """building block port, dynamic data structure. It stores input and output values and is assigned to bb executor """
    value: Any | None

    @validator("value")
    def check_value(cls, port_value, values):
        port_name = values["name"]
        port_type = values["port_type"]

        if isinstance(port_value, port_type):
            return port_value
        else:
            try:
                port_value = port_type(port_value)
            except Exception as e:
                if port_value is None:
                    return port_value
                else:
                    raise TypeError(
                        f" The value type of building block port '{port_name}' does not comply with the given type '{port_type}'.Type of the given value: {type(port_value)}")
            else:
                return port_value

    class Config:
        validate_assignment = True


TBBPort = TypeVar('TBBPort', bound=BuildingBlockPortDataStructure)  # generic type: building block port
TBBEPort = TypeVar('TBBEPort', bound=BuildingBlockPortWithValues)  # genetic type of bb executor port
TLH = TypeVar('TLH', bound=LocalLogHandler)  # generic type: log handler


class BuildingBlockDataStructure(BaseModel):
    name: str = ''
    architecture: str = ''
    version: str = ''
    description: str = ''
    category: str = 'undefined'

    _inlet_ports: dict[str, TBBPort] = {}
    _outlet_ports: dict[str, TBBPort] = {}

    _settings: dict = {}
    interactive_settings: bool = False
    pipeline_manager: object = None
    logger: TLH

    @property
    def settings(self):
        return self._settings

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        copy_on_model_validation = 'none'
        underscore_attrs_are_private = True
        extra = "allow"


TBB = TypeVar('TBB', bound=BuildingBlockDataStructure)
TV = TypeVar('TV', bound=Visualizer)
TGUI= TypeVar('TGUI', bound=AbstractInteractiveGUI)


class BuildingBlockExecutorDataStructure(BaseModel):
    building_block: TBB
    visualizer: TV = None
    interactive_gui: TGUI = None
    execution_mode: str = "undefined"

    bb_status: int = -1
    _execution_status: int = -1

    execution_start: datetime = None
    execution_end: datetime = None
    execution_time: float = None

    inlet_ports_dict: dict[str, TBBEPort] = {}  # new change: dict contains inlet port with values
    outlet_ports_dict: dict[str, TBBEPort] = {}  # new change: dict contains outlets port with values

    logger: TLH

    interactive_configuration: bool = False
    interactive_gui_endpoint: str = ''

    visualization_endpoint: str = ''
    visualizer_module: str = 'undefined'
    visualizer_class: str = 'undefined'

    settings: dict = {}

    @property
    def execution_status(self):
        return self._execution_status

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        copy_on_model_validation = 'none'
        underscore_attrs_are_private = True
        # extra = "allow"


TBE = TypeVar('TBE', bound=BuildingBlockExecutorDataStructure)
TTP = TypeVar('TTP', bound=TopologyProvider)
# TC = TypeVar('TC', bound=ConnectionInformation)

class PipelineDataStructure(PipelineInformation):
    topology_provider: TTP = None
    nodes: dict[str, TBB] = {}
    connections: dict[str, Any] = {}
    pipeline_manager:object = None

    @validator("nodes", pre=True)
    def check_node(cls, nodes):
        for node in nodes.values():
            if not isinstance(node, BuildingBlockDataStructure):
                raise ValidationError
        return nodes

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        copy_on_model_validation = 'none'

TThread = TypeVar('TThread', bound=Thread)
TPL = TypeVar('TPL', bound=PipelineDataStructure)

class PipelineExecutorDataStructure(BaseModel):
    pipeline: TPL
    port_generator: PortNumberCounter = None
    execution_mode: str = 'undefined'
    pipeline_execution: dict[str, TBE] = {}
    execution_sequence: list[TBB] = []
    _execution_status: int = -1
    config: Any = None
    logger: TLH
    host: str = '127.0.0.1'

    @property
    def execution_status(self):
        return self._execution_status

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        copy_on_model_validation = 'none'
        extra = "allow"


TPipelineExecutor = TypeVar('TPipelineExecutor', bound=PipelineExecutorDataStructure)
