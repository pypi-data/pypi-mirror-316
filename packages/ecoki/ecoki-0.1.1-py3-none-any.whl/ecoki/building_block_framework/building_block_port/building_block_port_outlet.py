from ecoki.building_block_framework.building_block_port.building_block_port import BuildingBlockPort
from typing import Optional


class BuildingBlockPortOutlet(BuildingBlockPort):
    """
        Class of Building Block Outlet Port, inherits from base class Building Block Port

        Attributes
        ----------
        name : str
            building block port name
        category : str
            building block port category: outlet
        port_type: type
            data type of building block port value, used to validate port value
        data_type : str
            data type of building block port value, used for RESTAPI response
        value (alias: default):
            building block port value, value type should be comply with the port_type
        allowed_data_types : list
            allowed data types of building block port
        status_code: int
            indicate the status of building block port (0: normal, 1: abnormal)
        """

    status_code: Optional[int]

    def set_status_code(self, status_code):
        """
        set status code to building block outlet port
        :param status_code: building block outlet port status 0: normal, 1: abnormal
        """
        self.status_code = status_code

    def get_status_code(self):
        """
        get status of building block outlet port
        :return: building block outlet port status 0: normal, 1: abnormal
        """
        return self.status_code

    def get_result(self):
        """
        get result from building block outlet port in dict
        :return: {name: value, "status_code": status_code}
        """
        return {self.name: self.get_port_value(), "status_code": self.get_status_code()}
    
    def get_port_info(self):
        """
        get building block port info in dict
        :return: building block port info dictionary {"name": name, "type": port_type, "value": value, "status_code": status_code}
        """
        return {"name": self.get_port_name(), "type": self.get_port_type(), "value": self.get_port_value(),
                "status_code": self.get_status_code()}
