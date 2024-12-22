# Project imports
from ecoki.visualizer_framework.visualizer import Visualizer
import panel as pn


class DataStorageManagementVisualization(Visualizer):
    """Building block for visualizing tabular data interactively."""

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.app = None
        self.panel_widgets_list = []

    def run(self):
        self.terminate()
        results = self.input_dict['input_data']
        collection_list = results["collection_list"]
        database_name = results["database_name"]
        self.visualize_each_database(database_name, collection_list)
        panel_column = pn.Column(width=800)
        panel_column.append("# Overview of created Database")
        panel_column.append(self.panel_widgets_list[0])
        panel_column.show(open=False, threaded=True, port=self.port,
                                                websocket_origin=f'127.0.0.1:{self.port}')

    def visualize_each_database(self, database_name, collection_list):
        static_text = pn.widgets.StaticText(name='Database', value=database_name)
        static_text_1 = pn.widgets.StaticText(name='Number of collections', value=len(collection_list))
        collection_list_selector = pn.widgets.Select(name='Existing collections', options=collection_list)
        self.panel_widgets_list.append(pn.Column(static_text, static_text_1, collection_list_selector))

    def terminate(self):
        if self.app:
            self.app.stop()
