# System imports
import numpy as np
import panel as pn
from functools import partial
from bokeh.models import ColumnDataSource, Div, Label, Range1d
from bokeh.plotting import figure
from bokeh.palettes import Category20 as palette
import pandas as pd
import itertools
from bokeh.palettes import inferno# select a palette
from bokeh.models import HoverTool, LinearAxis, Range1d, DataRange1d, DataRange
from datetime import timedelta
# Project imports
from ecoki.visualizer_framework.visualizer import Visualizer

def create_hovertool_spec(columns, x_axis):
    spec = []
    for column in columns:
        if column == "timestamp":
            spec.append((x_axis, "@" + x_axis + "{%c}"))
        else:
            spec.append((column, "@{" + column + "}"))
    return spec


def update_div(data_source, columns, x_axis):
    div_str = """<h3> Latest Measurements</h3><p> """
    for column in columns:
        if column == x_axis:
            div_str += f"<b>{column}</b>: {data_source[column][-1]} <br>"
        else:
            div_str += f"<b>{column}</b>: {np.round(data_source[column][-1], 5)} <br>"
    div_str += """</p>"""

    return div_str


def update_label(data_source, columns, x_axis):
    x_coordinate = data_source[x_axis][-1]
    y_coordinate = np.round(data_source[list(columns)[-1]][-1], 5)
    label_str = ""
    for column in columns:
        if column == x_axis:
            label_str += f"{column}: {data_source[column][-1]} \n"
        else:
            label_str += f"{column}: {np.round(data_source[column][-1], 5)} \n"

    return x_coordinate, y_coordinate, label_str


class LiveDataVisualizer(Visualizer):
    """Building block for visualizing tabular data interactively."""

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.data = None
        self.source = None
        self.p = figure(width=1800, height=800, x_axis_type="datetime")  # plot
        # self.p.add_tools(HoverTool(tooltips=TOOLTIPS, mode="vline"))  # add hover tool to show values
        self.periodic_callback = None  # callback to update data with new data in the plot
        self.colors = itertools.cycle(palette[20])      # color container for different lines
        self.div = Div(text='')  # additional section to show values
        self.dynamic_label = None
        self.columns = []
        self.x_axis = None

    def run(self):
        new_data = self.input_dict["input_data"]

        #if not new_data.index.name:  # if the input dataset does not have an index column
        #    pass
        #else:
        #try:
        #    new_data.index.names = ["timestamp"]  # if the index column of input dataset is not called "timestamp"
        #except Exception as e:
        #    pass
        if not self.x_axis:
            self.x_axis = new_data.index.name
        new_data.reset_index(inplace=True)

        new_data[self.x_axis] = pd.to_datetime(new_data[self.x_axis])  # convert string timestamp to datetime

        #print(new_data["timestamp"])
        new_data_list = new_data.to_dict("list")  # convert dataframe to dict (easy to handle in bokeh)

        if "index" in new_data_list.keys():
            del new_data_list["index"]

        if self.data:
            for column in self.columns:
                self.data[column].extend(new_data_list[column])  # append new data
        else:
            self.data = new_data_list
            self.columns = self.data.keys()

        if self.source is None:
            self.p.add_tools(HoverTool(tooltips=create_hovertool_spec(self.columns, self.x_axis), formatters={f'@{self.x_axis}': 'datetime'}, mode="mouse"))  # add hover tool to show values
            self.source = ColumnDataSource(data=self.data)  # initiate data source

            self.source.stream(self.data)  # inject first data points

            #x_coordinate, y_coordinate, label_str = update_label(self.source.data, self.columns)

            #self.dynamic_label = Label(x=x_coordinate, y=y_coordinate,
            #                           text=label_str,
            #                           x_offset=timedelta(seconds=200).total_seconds() * -1,
            #                           y_offset=50)

            #self.p.add_layout(self.dynamic_label)

            self.div.text = update_div(self.source.data, columns=self.columns, x_axis=self.x_axis)  # update latest measurement division


            # draw lines
            for num, column in enumerate(self.columns):
                if column == self.x_axis:
                    pass
                else:
                    color = next(self.colors)
                    line = self.p.line(x=self.x_axis, y=column,
                                       source=self.source,
                                       legend_label=column,
                                       width=4,
                                       color=color,
                                       alpha=0.8,
                                       muted_color=color, muted_alpha=0.2,
                                       y_range_name=column
                                       )
                    line.visible = True if num == 1 or num == 2 else False
                    self.p.extra_y_ranges[column] = DataRange1d(only_visible=True) # add y-axis for each individual measurement
                    self.p.extra_y_ranges[column].renderers = [line]
                    self.p.add_layout(LinearAxis(axis_label=column, y_range_name=column), 'left')
                    next(self.colors)
            self.p.legend.location = "top_left"
            self.p.legend.click_policy = "hide"

            def update(source):
                # steam closes the line from the end of new data to the end of old data point...
                # self.source.stream(self.data)

                self.source.data.update(self.data)

                # update details section
                self.div.text = update_div(self.source.data, columns=self.columns, x_axis=self.x_axis)

                #x_coordinate, y_coordinate, label_str = update_label(self.source.data, self.columns)
                #self.dynamic_label.x = x_coordinate
                #self.dynamic_label.y = y_coordinate
                #self.dynamic_label.text = label_str

            self.periodic_callback = pn.state.add_periodic_callback(partial(update, self.source), 200, timeout=200000)
            toggle = pn.widgets.Toggle(name='Start Real-Time Visualization', value=True)
            toggle.link(self.periodic_callback, bidirectional=True, value='running')

            self.visualizer = pn.Column(pn.Row(pn.pane.Bokeh(self.p), self.div), toggle)
            self._show_visualizer()
            #pn.serve(self.visualizer, threaded=True)

    def terminate(self):
        if self.app:
            self.source = None
            self.p = figure(width=1800, height=800, x_axis_type="datetime")
            self.periodic_callback.stop()
            self.periodic_callback = None
            self.app.stop()
            self.app = None
