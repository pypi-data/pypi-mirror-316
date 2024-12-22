from ecoki.visualizer_framework.visualizer import Visualizer

import panel as pn
import hvplot.pandas


class TabularDataDashboard:
    def __init__(self, df):
        self.df = df

        # Create widgets
        start_date = self.df.index[0]
        end_date = self.df.index[-1]
        # self.widget_datetime_range = pn.widgets.DatetimeRangeInput(name='Select datetime range',
        #                                                            start=start_date,
        #                                                            end=end_date,
        #                                                            value=(start_date,
        #                                                                   end_date
        #                                                                   )
        #                                                            )

    def create_view(self, accent="#00A170"):

        # Create Row panel for interactive Bokeh plots
        panel_plots = pn.Tabs()
        panel_plots.append(("Horizontal Bar plot", self.df.hvplot(title="Feature Importance",
                                                            kind="barh",
                                                            grid=True,
                                                        responsive=True,
                                                            height=400)))

        dashboard = pn.template.MaterialTemplate(
            site="ecoKI", title="Feature Importance Dashboard",
            main=[
                panel_plots
            ],
            # accent=accent
        )

        return dashboard



class TrainAndPredictXGBoostVisualizer(Visualizer):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def run(self):
        self.terminate()
        # df = self.building_block.get_port_value(port_name='output_data_featimp', port_direction='outlet')
        df = self.input_dict['output_data_featimp']
        dashboard = TabularDataDashboard(df)
        self.visualizer = dashboard.create_view()
        self._show_visualizer()