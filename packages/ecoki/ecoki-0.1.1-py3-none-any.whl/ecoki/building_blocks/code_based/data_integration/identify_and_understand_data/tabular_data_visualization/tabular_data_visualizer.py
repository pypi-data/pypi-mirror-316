# System imports
from pandas import DataFrame

# Project imports
from ecoki.visualizer_framework.visualizer import Visualizer
from ecoki.building_blocks.code_based.data_integration.identify_and_understand_data.tabular_data_visualization.bokeh_dashboard import TabularDataDashboard


class TabularDataVisualizer(Visualizer):
    """Building block for visualizing tabular data interactively."""

    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def run(self):
        self.terminate()
        # df = self.building_block.get_port_value(port_name='output_data', port_direction='outlet')
        df = self.input_dict["input_data"]
        dashboard = TabularDataDashboard(df)
        self.visualizer = dashboard.create_view()
        self._show_visualizer()
