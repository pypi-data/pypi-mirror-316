# System imports
import panel as pn
import hvplot.pandas
import pandas as pd

pn.extension()

# Project imports
from ecoki.visualizer_framework.visualizer import Visualizer


class EnergyMonitoringDashboard:
    def __init__(self, df):
        self.df = df
        self.df.index = pd.to_datetime(self.df.index)
        self.columns_select = pn.widgets.MultiSelect(name='Select columns', value=list(self.df.columns),
                                                     options=list(self.df.columns))
        self.date_range_select = pn.widgets.DatetimeRangePicker(name='Timeframe',
                                                                value=(self.df.index[0].to_pydatetime(),
                                                                       self.df.index[-1].to_pydatetime()))
        self.reset_button = pn.widgets.Button(name='Reset', button_type='primary')

        def b(event):
            self.date_range_select.value = (self.df.index[0].to_pydatetime(), self.df.index[-1].to_pydatetime())

        self.reset_button.on_click(b)
        self.granularity_select = pn.widgets.Select(name='Granularity', options={'Default': '-',
                                                                                 'Hour': 'H',
                                                                                 'Day': 'D',
                                                                                 'Week': 'W',
                                                                                 'Month': 'M',
                                                                                 'Year': 'Y'})
        self.total_energy = pn.widgets.Checkbox(name='Sum selected columns')

    def filtered_df(self, date_range_select, columns_select, granularity_select, total_energy):
        res = self.df.loc[date_range_select[0]:date_range_select[-1]][columns_select]
        if granularity_select != '-':
            res = res.resample(granularity_select).sum()
        if total_energy:
            res["Total"] = res.sum(axis=1)

        return res

    def plot(self):
        dfi = hvplot.bind(self.filtered_df, self.date_range_select, self.columns_select, self.granularity_select,
                          self.total_energy).interactive()
        return dfi.hvplot(kind='line', alpha=0.7, grid=True, ylabel="Wh", height=500, width=1000, legend="top").apply.opts(framewise=True)

    def create_view(self):
        # Create interactive plot
        energy_plot = self.plot()

        # Define dashboard components
        panel_plot = pn.Column(pn.pane.Markdown('## Energy Consumption', align='center'),
                               energy_plot.panel(),
                               background='WhiteSmoke')
        panel_date_selectors = pn.Column(pn.pane.Markdown('## Date Selection Options', align='center'),
                                         self.granularity_select,
                                         self.date_range_select,
                                         self.reset_button,
                                         background='WhiteSmoke')
        panel_total_energy = pn.Column(pn.pane.Markdown('## Total Energy Consumption', align='center'),
                                       self.total_energy,
                                       background='WhiteSmoke')
        panel_columns = pn.Column(pn.pane.Markdown('## Energy Columns Selection', align='center'),
                                  self.columns_select,
                                  background='WhiteSmoke')

        dashboard = pn.template.MaterialTemplate(title='Energy Monitoring Dashboard')

        # Add components to dashboard
        dashboard.main.append(pn.Row(panel_plot,
                                     pn.layout.HSpacer(),
                                     pn.Column(panel_columns, pn.layout.VSpacer(), panel_date_selectors,
                                               pn.layout.VSpacer(), panel_total_energy)
                                     )
                              )
        # dashboard.sidebar.append(self.columns_select)

        return dashboard


class EnergyDataVisualizer(Visualizer):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def run(self):
        self.terminate()
        df = self.input_dict["input_data"]
        dashboard = EnergyMonitoringDashboard(df)
        self.visualizer = dashboard.create_view()
        self._show_visualizer()
