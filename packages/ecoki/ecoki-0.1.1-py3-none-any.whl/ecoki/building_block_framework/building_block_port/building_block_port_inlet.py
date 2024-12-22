from ecoki.building_block_framework.building_block_port.building_block_port import BuildingBlockPort
from typing import Optional, Any
from pydantic import Field


class BuildingBlockPortInlet(BuildingBlockPort):
    """
        Class of Building Block Inlet Port, inherits from base class Building Block Port

        Attributes
        ----------
        name : str
            building block port name
        category : str
            building block port category: inlet
        port_type: type
            data type of building block port value, used to validate port value
        data_type : str
            data type of building block port value, used for RESTAPI response
        value (alias: default):
            building block port value, value type should be comply with the port_type
        allowed_data_types : list
            allowed data types of building block port
        """

    def get_port_info(self):
        """
        get building block port info in dict
        :return: building block port info dictionary {"name": name, "type": port_type, "value": value}
        """
        return {"name": self.get_port_name(), "type": self.get_port_type(), "value": self.get_port_value()}