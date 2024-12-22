from abc import ABC, abstractmethod
from ecoki.common.base_classes import PortInformation, PortInformationWithValues, BuildingBlockPortWithValues
from pandas import DataFrame
import json

"""
Building block port class is now the base class for bb ports that contain values. The input and output port subclasses will be assigned to bb executor not bb class
"""
class BuildingBlockPort(ABC, BuildingBlockPortWithValues):
    """
        Base class of Building Block Port, inherits from data structure  BuildingBlockPortWithValues

        Attributes
        ----------
        name : str
            building block port name
        category : str
            building block port category: inlet or outlet
        port_type: type
            data type of building block port value, used to validate port value
        data_type : str
            data type of building block port value, used for RESTAPI response
        value:
            building block port value, value type should be comply with the port_type
        allowed_data_types : list
            allowed data types of building block port
    """

    def get_port_name(self):
        """
        get building block port name
        """
        return self.name

    def get_port_type(self):
        """
        get data type of the building block port
        """
        return self.port_type

    def get_port_type_name(self):
        """
        get data type of the building block port in string
        """
        return self.data_type

    def get_port_value(self):
        """
        get building block port value
        """
        return self.value

    def set_port_value(self, value):
        """
       set value to building block port
       :param value: building block port value
       """
        self.value = value

    @abstractmethod
    def get_port_info(self):
        pass

    def get_info_obj(self):
        """
        get building block port information for RestApi
        :return: Data structure PortInformation
        """
        return PortInformation(name=self.get_port_name(),
                               data_type=self.get_port_type_name(),
                               category=self.category,
                               allowed_data_types=[])

    def get_info_obj_with_values(self):
        """
        get building block port information and values for RestApi
        :return: Data structure obj PortInformationWithValues
        """
        values = self.get_port_value()
        if isinstance(values, DataFrame):
            values_json = values.to_json()
        elif isinstance(values, (int, float)):
            values_json = values
        else:
            try:
                values_json = json.dumps(values)
            except Exception as exc:
                values_json = f'Cannot convert to json: {exc}'

        return PortInformationWithValues(name=self.get_port_name(),
                                         data_type=self.get_port_type_name(),
                                         category=self.category,
                                         values=values_json,
                                         allowed_data_types=[])
