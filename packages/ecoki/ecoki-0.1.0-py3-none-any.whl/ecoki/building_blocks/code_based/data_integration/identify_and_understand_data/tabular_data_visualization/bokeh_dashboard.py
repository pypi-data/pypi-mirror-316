# System imports
import panel as pn
import hvplot.pandas


class TabularDataDashboard:
    def __init__(self, df):
        self.df = df

        # Create widgets
        self.widget_selected_columns = pn.widgets.MultiSelect(name='Select columns', value=list(self.df.columns),
                                                              options=list(self.df.columns))

        self.widget_highlight_nan = pn.widgets.Toggle(name='Highlight NaN values')

        self.widget_highlight_duplicates = pn.widgets.Toggle(name='Highlight duplicates')

        # Widgets to configure scatter plot
        self.widget_scatter_plot_x = pn.widgets.Select(name='x-axis', options=list(self.df.columns))
        self.widget_scatter_plot_y = pn.widgets.Select(name='y-axis', options=list(self.df.columns))
        self.widget_scatter_plot_z = pn.widgets.Select(name='3rd dimension', options=list(self.df.columns))

    def highlight_dataframe_cells(self,
                                  data_frame,
                                  highlight_nan,
                                  highlight_duplicates,
                                  nan_color="#00A170",
                                  duplicates_color='yellow'):
        res = data_frame.style
        if highlight_nan:
            res = res.highlight_null(color=nan_color)
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

        panel_table = pn.Tabs(("Data table", self.to_tabulator(styled_df).panel()))
        panel_table.append(("Descriptive statistics", self.to_tabulator(filtered_df.describe(include="all")).panel()))

        # Create Row panel for interactive Bokeh plots
        panel_plots = pn.Tabs()
        panel_plots.append(("Line plot", filtered_df.hvplot(title="Line Plot",
                                                            kind="line",
                                                            grid=True,
                                                            responsive=True,
                                                            height=400).panel()))
        panel_plots.append(("Histogram", filtered_df.hvplot(title="Histogram",
                                                            kind="hist",
                                                            alpha=0.7,
                                                            grid=True,
                                                            responsive=True,
                                                            height=400).panel()))
        panel_plots.append(("Scatter plot", self.df.hvplot(title="Scatter Plot",
                                                           kind="scatter",
                                                           x=self.widget_scatter_plot_x,
                                                           y=self.widget_scatter_plot_y,
                                                           c=self.widget_scatter_plot_z,
                                                           alpha=0.2,
                                                           grid=True,
                                                           responsive=True,
                                                           height=400)))

        dashboard = pn.template.MaterialTemplate(
            site="ecoKI", title="Tabular Dataset Visualization Dashboard",
            sidebar=[
                pn.WidgetBox("### Formatting options",
                             self.widget_highlight_nan,
                             self.widget_highlight_duplicates
                             ),

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
                panel_plots
            ],
        )

        return dashboard
