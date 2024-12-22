# System imports
from pandas import DataFrame

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock
from ecoki.building_blocks.code_based.data_integration.identify_and_understand_data.tabular_data_visualization.bokeh_dashboard import TabularDataDashboard


class TabularDataVisualization(BuildingBlock):
    """Building block for visualizing tabular data interactively."""

    def __init__(self, name, settings):
        super().__init__(name, settings)
        self.architecture = "EcoKI"
        self.version = "1"
        self.description = "Create an interactive dashboard to visualize a tabular dataset passed as input. \
                            The dashboard offers the following possibilities: \n \
                            - Line plots, histograms and correlation plots of the data, \n \
                            - Summary statistics table, \n \
                            - Sort/filter table, \n \
                            - Select the columns to display, \n \
                            - Highlight duplicates and missing values"
        self.category = "DataVisualizer"  # TODO: What are all BB categories?
        self.add_inlet_port('input_data', DataFrame)
        self.app = None

    def execute(self):
        if self.app:
            self.app.stop()
        df = self.inlet_ports['input_data'].get_port_value()
        dashboard = TabularDataDashboard(df)
        self.app = dashboard.create_view().show(threaded=True, port=5500, websocket_origin=['*'])
