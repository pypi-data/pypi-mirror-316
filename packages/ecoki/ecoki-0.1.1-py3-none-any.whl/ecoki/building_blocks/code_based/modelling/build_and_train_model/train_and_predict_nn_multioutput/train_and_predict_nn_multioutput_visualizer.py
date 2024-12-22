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
    def __init__(self, df, featimp = None, metrics = None, hyperparameters = None, label_column = None):
        """
        Initializes the TabularDataDashboard class.

        Args:
        - df: pandas DataFrame
            The input data.
        - featimp: pandas DataFrame, default None
            The feature importances.
        - metrics: dict, default None
            The evaluation metrics.
        - hyperparameters: pandas DataFrame, default None
            The hyperparameters.
        - label_column: pandas DataFrame, default None
            The label column.
        """
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

        Returns:
        - pn.widgets.Tabulator or pn.pane.Markdown
            The feature importance view.
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

        Returns:
        - pn.Row or pn.pane.Markdown
            The bar plot view.
        """
        if self.featimp is not None:
            targets = []
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

        Returns:
        - pn.pane.HTML
            The model summary view.
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
            mse_value = self.metrics[f'mse_{self.label_column[0].values[i]}']
            mse_value = mse_value.iloc[0]  # Get the first value from the Series
            model_summary += f"<p class='text'>Mean Squared Error for {self.label_column[0].values[i]}: {mse_value}</p>"

        model_summary += "</div>"

        return pn.pane.HTML(model_summary)

    def create_hyperparameters_view(self):
        """
        Creates a view for the hyperparameters.

        Returns:
        - pn.widgets.Tabulator or pn.pane.Markdown
            The hyperparameters view.
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

        Returns:
        - None
        """
        nodes = [
            "Start",
            "Split the input data into training and test sets",
            "Create XGBoost regressor and Multi-output regressor",
            "Train the Multi-output model",
            "Save and load the trained model",
            "Make predictions on the test set",
            "Evaluate the model using Mean Squared Error",
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
            ("Make predictions on the test set", "Evaluate the model using Mean Squared Error"),
            ("Evaluate the model using Mean Squared Error", "Store and save true values and predicted values"),
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

    def highlight_dataframe_cells(self,
                                  data_frame,
                                  highlight_nan,
                                  highlight_duplicates,
                                  nan_color="#00A170",  # 'orange',
                                  duplicates_color='yellow'):
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
        """Filter dataset according to widget values (selected columns, date slider value, etc).
        """

        res = None
        if df is not None:
            df_i = df.interactive()
            # res = df_i.loc[self.widget_datetime_range.value[0]:self.widget_datetime_range.value[-1]][self.widget_selected_columns]
            res = df_i[self.widget_selected_columns]

        return res

    def style_dataframe(self, df):
        res = None
        if df is not None:
            res = df.pipe(self.highlight_dataframe_cells, self.widget_highlight_nan, self.widget_highlight_duplicates)

        return res

    def to_tabulator(self, df):
        """Wrap interactive DataFrame in a Tabulator widget
        """
        return df.pipe(pn.widgets.Tabulator,  # TODO: add header filters
                       disabled=True,
                       pagination='remote',
                       layout='fit_columns',
                       page_size=10,
                       sizing_mode='stretch_width')

    def create_view(self, accent="#00A170"):
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

        #panel_plots.append(("Feature Importance barplot", self.create_feature_importance_bar_plot()))

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


class TrainAndPredictNNMultiVisualizer(Visualizer):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def run(self):
        self.terminate()
        df = self.input_dict['output_data_preds']
        featimp = self.input_dict['output_data_featimp']
        metrics = self.input_dict['output_data_metrics']
        hyperparameters = self.input_dict['output_data_hyperparameters']
        label_column = self.input_dict['output_data_labels']
        dashboard = TabularDataDashboard(df, featimp = featimp, metrics = metrics,hyperparameters = hyperparameters, label_column=label_column)
        self.visualizer = dashboard.create_view()
        self._show_visualizer()