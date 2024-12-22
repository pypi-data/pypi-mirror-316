from ecoki.building_block_framework.building_block import BuildingBlock


class StaticValue(BuildingBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Read static values from setting"
        self.version = "1"
        self.category = "Data source"

        self.add_outlet_port('output_data', object)

    def execute(self):
        # port_output_data = self.get_port('output_data', 'outlet')

        data = self.settings['value']

        return {"output_data": data}
        # port_output_data.set_port_value(data)
        # port_output_data.set_status_code(0)
