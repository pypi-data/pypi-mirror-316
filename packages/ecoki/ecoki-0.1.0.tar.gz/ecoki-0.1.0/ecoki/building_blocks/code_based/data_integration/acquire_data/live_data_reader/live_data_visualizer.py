# System imports
import numpy as np
import panel as pn
from functools import partial
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
import pandas as pd
from itertools import cycle
import json

# Project imports
from ecoki.visualizer_framework.visualizer import Visualizer
from ecoki.building_blocks.code_based.data_integration.identify_and_understand_data.tabular_data_visualization.bokeh_dashboard import \
    TabularDataDashboard


class LiveDataVisualizer(Visualizer):
    """Building block for visualizing tabular data interactively."""

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.data = None
        self.source = None
        self.p = figure(width=1800, height=800, x_axis_type="datetime")
        self.periodic_callback = None

    def run(self):
        # self.terminate()

        self.data = self.input_dict["input_data"]

        colors = cycle(palette)

        if self.source is None:
            self.source = ColumnDataSource(pd.DataFrame(columns=self.data.columns))
            self.source.stream(self.data)

            for column in self.data.keys():
                if column == "timestamp":
                    pass
                else:
                    self.p.line(x="timestamp", y=column,
                                source=self.source,
                                legend_label=column,
                                width=4,
                                color=next(colors)
                                )

            def update(source):
                self.source.stream(self.data)

            self.periodic_callback = pn.state.add_periodic_callback(partial(update, self.source), 100, timeout=20000)
            toggle = pn.widgets.Toggle(name='Start Real-Time Visualization', value=True)
            toggle.link(self.periodic_callback, bidirectional=True, value='running')

            self.visualizer = pn.Column(pn.pane.Bokeh(self.p), toggle)
            self._show_visualizer()

    def terminate(self):
        if self.app:
            self.source = None
            self.p = figure(width=1800, height=800, x_axis_type="datetime")
            self.periodic_callback.stop()
            self.periodic_callback = None
            self.app.stop()
            self.app = None
