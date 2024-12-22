from ecoki.visualizer_framework.visualizer import Visualizer

import panel as pn
import hvplot.pandas
import pandas as pd
import networkx as nx
import holoviews as hv
from holoviews import opts
from networkx import spring_layout
from bokeh.plotting import figure, show, output_file
from bokeh.models import BoxAnnotation, Label, LabelSet, ColumnDataSource, Arrow, OpenHead
from bokeh.io import output_notebook
from bokeh.layouts import column
from bokeh.embed import components
import graphviz

hv.extension('bokeh')

class TabularDataDashboard:
    """
    A dashboard for visualizing tabular data, feature importances, model metrics, hyperparameters, and process flowchart.

    Parameters
    ----------
    df : pandas.DataFrame
        The input data.
    featimp : pandas.DataFrame, optional
        The feature importances. Default is None.
    metrics : dict, optional
        The evaluation metrics. Default is None.
    hyperparameters : pandas.DataFrame, optional
        The hyperparameters. Default is None.
    label_column : pandas.DataFrame, optional
        The label column. Default is None.

    Attributes
    ----------
    df : pandas.DataFrame
        The input data.
    featimp : pandas.DataFrame
        The feature importances.
    metrics : dict
        The evaluation metrics.
    hyperparameters : pandas.DataFrame
        The hyperparameters.
    label_column : pandas.DataFrame
        The label column.
    widget_selected_columns : pn.widgets.MultiSelect
        Widget for selecting columns.
    widget_highlight_nan : pn.widgets.Toggle
        Widget for highlighting NaN values.
    widget_highlight_duplicates : pn.widgets.Toggle
        Widget for highlighting duplicates.
    widget_scatter_plot_x : pn.widgets.Select
        Widget for selecting x-axis in scatter plot.
    widget_scatter_plot_y : pn.widgets.Select
        Widget for selecting y-axis in scatter plot.
    widget_scatter_plot_z : pn.widgets.Select
        Widget for selecting third dimension in scatter plot.
    """
    def __init__(self, df, featimp=None, metrics=None, hyperparameters=None, label_column=None):
        self.df = df
        self.featimp = featimp
        self.metrics = metrics
        self.hyperparameters = hyperparameters
        self.label_column = label_column

        self.widget_selected_columns = pn.widgets.MultiSelect(name='Select columns', value=list(self.df.columns),
                                                              options=list(self.df.columns))

        self.widget_highlight_nan = pn.widgets.Toggle(name='Highlight NaN values')

        self.widget_highlight_duplicates = pn.widgets.Toggle(name='Highlight duplicates')

        # Widgets to configure scatter plot
        self.widget_scatter_plot_x = pn.widgets.Select(name='x-axis', options=list(self.df.columns))
        self.widget_scatter_plot_y = pn.widgets.Select(name='y-axis', options=list(self.df.columns))
        self.widget_scatter_plot_z = pn.widgets.Select(name='3rd dimension', options=list(self.df.columns))

    def create_feature_importance_view(self):
        """
        Creates a view for the feature importance scores.

        Returns
        -------
        pn.widgets.Tabulator or pn.pane.Markdown
            The feature importance view, either as a tabulator widget or markdown text if feature importances are not available.
        """
        if self.featimp is not None:
            return self.featimp.pipe(pn.widgets.Tabulator,
                                                 disabled=True,
                                                 pagination='remote',
                                                 layout='fit_columns',
                                                 page_size=10,
                                                 sizing_mode='stretch_width')
        else:
            return pn.pane.Markdown("## Feature importances not available")

    def create_feature_importance_bar_plot(self):
        """
        Creates a bar plot for the feature importance scores.

        Returns
        -------
        pn.Row or pn.pane.Markdown
            The bar plot view, either as a row of plots or markdown text if feature importances are not available.
        """
        if self.featimp is not None:
            targets = self.label_column[0].values

            bar_plots = [self.featimp.hvplot.barh(y=target, height=400, grid=True).opts(title=target) for target in
                         targets]
            layout = pn.Row(*bar_plots)

            return layout

        else:
            return pn.pane.Markdown("## Feature importances not available")

    def create_model_summary_view(self):
        """
        Creates a view for the model summary.

        Returns
        -------
        pn.pane.HTML
            The model summary view, formatted as HTML.
        """
        model_summary = """
        <style>
            .summary {
                font-family: Arial, sans-serif;
            }
            .title {
                color: #003366;
            }
            .subtitle {
                color: #0077B6;
                font-weight: bold;
            }
            .text {
                color: #778DA9;
            }
        </style>
        <div class="summary">
            <h2 class="title">Model Summary</h2>
            <p class="subtitle">Model Type:</p>
            <p class="text">XGBoost Multi-output Regressor</p>
            <p class="subtitle">Model Performance:</p>
        """

        for i in range(len(self.label_column)):
            rmse_value = self.metrics[f'rmse_{self.label_column[0].values[i]}']
            rmse_value = rmse_value.iloc[0]  # Get the first value from the Series
            model_summary += f"<p class='text'>Root Mean Squared Error for {self.label_column[0].values[i]}: {rmse_value}</p>"

        model_summary += "</div>"

        return pn.pane.HTML(model_summary)

    def create_hyperparameters_view(self):
        """
        Creates a view for the hyperparameters.

        Returns
        -------
        pn.widgets.Tabulator or pn.pane.Markdown
            The hyperparameters view, either as a tabulator widget or markdown text if hyperparameters are not available.
        """
        if self.hyperparameters is not None:
            return self.hyperparameters.pipe(pn.widgets.Tabulator,
                                                 disabled=True,
                                                 pagination='remote',
                                                 layout='fit_columns',
                                                 page_size=10,
                                                 sizing_mode='stretch_width')
        else:
            return pn.pane.Markdown("## Hyperparameters not available")

    def create_process_flowchart(self):
        """
        Creates a process flowchart.

        Returns
        -------
        pn.pane.HTML
            The process flowchart, rendered as HTML.
        """
        nodes = [
            "Start",
            "Split the input data into training and test sets",
            "Create XGBoost regressor and Multi-output regressor",
            "Train the Multi-output model",
            "Save and load the trained model",
            "Make predictions on the test set",
            "Evaluate the model using Root Mean Squared Error",
            "Store and save true values and predicted values",
            "Retrieve and save feature importances",
            "End"
        ]

        edges = [
            ("Start", "Split the input data into training and test sets"),
            ("Split the input data into training and test sets", "Create XGBoost regressor and Multi-output regressor"),
            ("Create XGBoost regressor and Multi-output regressor", "Train the Multi-output model"),
            ("Train the Multi-output model", "Save and load the trained model"),
            ("Save and load the trained model", "Make predictions on the test set"),
            ("Make predictions on the test set", "Evaluate the model using Root Mean Squared Error"),
            ("Evaluate the model using Root Mean Squared Error", "Store and save true values and predicted values"),
            ("Store and save true values and predicted values", "Retrieve and save feature importances"),
            ("Retrieve and save feature importances", "End")
        ]

        # Create a Graphviz Digraph
        dot = graphviz.Digraph()
        dot.attr(rankdir="TB")

        # Add nodes
        for node in nodes:
            dot.node(node, fontname="Arial", fontsize="12", shape="box", style="filled", fillcolor="#E6F3FF",
                     width="0.75", height="0.4")
        # Add edges
        for edge in edges:
            dot.edge(*edge, fontname="Arial", fontsize="10", arrowhead="open", arrowsize="0.5")

        # Render the flowchart as SVG
        svg = dot.pipe(format="svg").decode("utf-8")

        return pn.pane.HTML(svg, sizing_mode="stretch_width")

    def highlight_dataframe_cells(self, data_frame, highlight_nan, highlight_duplicates, nan_color="#00A170", duplicates_color='yellow'):
        """
        Highlights cells in a DataFrame based on NaN values and duplicates.

        Parameters
        ----------
        data_frame : pandas.DataFrame
            The DataFrame to highlight.
        highlight_nan : bool
            Whether to highlight NaN values.
        highlight_duplicates : bool
            Whether to highlight duplicate rows.
        nan_color : str, optional
            The color for highlighting NaN values, by default "#00A170".
        duplicates_color : str, optional
            The color for highlighting duplicate rows, by default 'yellow'.

        Returns
        -------
        pandas.io.formats.style.Styler
            The styled DataFrame.
        """
        res = data_frame.style
        if highlight_nan:
            res = res.highlight_null(null_color=nan_color)
        if highlight_duplicates:
            rows_series = data_frame.duplicated(keep='first')
            rows = rows_series[rows_series].index.values

            res = res.apply(lambda x: ['background: ' + duplicates_color if x.name in rows
                                       else '' for i in x], axis=1)
        return res

    def filter_dataframe(self, df):
        """
        Filters the DataFrame based on widget values.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to filter.

        Returns
        -------
        pandas.DataFrame
            The filtered DataFrame.
        """
        res = None
        if df is not None:
            df_i = df.interactive()
            res = df_i[self.widget_selected_columns]

        return res

    def style_dataframe(self, df):
        """
        Styles the DataFrame based on widget configurations for highlighting.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to style.

        Returns
        -------
        pandas.io.formats.style.Styler
            The styled DataFrame.
        """
        res = None
        if df is not None:
            res = df.pipe(self.highlight_dataframe_cells, self.widget_highlight_nan, self.widget_highlight_duplicates)

        return res

    def to_tabulator(self, df):
        """
        Wraps an interactive DataFrame in a Tabulator widget.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to wrap.

        Returns
        -------
        pn.widgets.Tabulator
            The DataFrame wrapped in a Tabulator widget.
        """
        return df.pipe(pn.widgets.Tabulator,
                       disabled=True,
                       pagination='remote',
                       layout='fit_columns',
                       page_size=10,
                       sizing_mode='stretch_width')

    def create_view(self, accent="#00A170"):
        """
        Creates the dashboard view.

        Parameters
        ----------
        accent : str, optional
            The accent color for the dashboard, by default "#00A170".

        Returns
        -------
        pn.template.MaterialTemplate
            The dashboard view.
        """
        filtered_df = self.filter_dataframe(self.df)
        styled_df = self.style_dataframe(filtered_df)

        panel_table = pn.Tabs(("Model summary", self.create_model_summary_view()))
        panel_table.append(("Model predictions", self.to_tabulator(styled_df).panel()))
        panel_table.append(("Feature Importances", self.create_feature_importance_view()))
        panel_table.append(("Hyperparameters", self.create_hyperparameters_view()))

        # Create Row panel for interactive Bokeh plots
        panel_plots = pn.Tabs()
        panel_plots.append(("Line plot", filtered_df.hvplot(title="Line Plot",
                                                            kind="line",
                                                            grid=True,
                                                            responsive=True,
                                                            height=400).panel()))

        panel_plots.append(("Feature Importance barplot", self.create_feature_importance_bar_plot()))

        process_flowchart = self.create_process_flowchart()

        dashboard = pn.template.MaterialTemplate(
            site="ecoKI", title="Prediction results Dashboard",
            sidebar=[

                pn.WidgetBox("### Plots settings",
                             self.widget_selected_columns,
                             pn.Column("Scatter plot",
                                       self.widget_scatter_plot_x,
                                       self.widget_scatter_plot_y,
                                       self.widget_scatter_plot_z
                                       )
                             )
            ],
            main=[
                panel_table,
                panel_plots,
                pn.pane.Markdown("## Machine learning process flow"),  # Add a heading for the flowchart
                process_flowchart
            ],
            # accent=accent
        )

        return dashboard


class TrainAndPredictXGBoostMultiVisualizer(Visualizer):
    """
    A visualizer for training and predicting with an XGBoost multi-output model.

    Inherits from the Visualizer class.

    Methods
    -------
    run():
        Executes the visualization process.
    """
    def __init__(self, **kwarg):
        """
        Initializes the TrainAndPredictXGBoostMultiVisualizer with given keyword arguments.

        Parameters
        ----------
        **kwarg : dict
            Keyword arguments for the Visualizer superclass.
        """
        super().__init__(**kwarg)

    def run(self):
        """
        Executes the visualization process, creating and displaying the dashboard.
        """
        self.terminate()
        df = self.input_dict['output_data_preds']
        featimp = self.input_dict['output_data_featimp']
        metrics = self.input_dict['output_data_metrics']
        hyperparameters = self.input_dict['output_data_hyperparameters']
        label_column = self.input_dict['output_data_labels']
        dashboard = TabularDataDashboard(df, featimp=featimp, metrics=metrics, hyperparameters=hyperparameters, label_column=label_column)
        self.visualizer = dashboard.create_view()
        self._show_visualizer()