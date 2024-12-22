# System imports
import pandas as pd

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock


class TimeSeriesResampler(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._architecture = "EcoKI"
        self._name = "TimeSeriesResampler"
        self._version = "1"
        self._description = "Building block for down- and upsampling time series data passed as a pandas DataFrame."
        self._category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', pd.DataFrame)

    def execute(self, input_data):
        on = None
        if 'on' in self.settings:
            on = self.settings['on']

        frequency = "W"
        if 'frequency' in self.settings:
            frequency = self.settings['frequency']

        aggregation_fct = "sum"
        if 'aggregation_fct' in self.settings:
            aggregation_fct = self.settings['aggregation_fct']

        # Read input json string as pandas DataFrame
        data = input_data
        data.index = pd.to_datetime(data.index)

        # Downsampling options
        if aggregation_fct == "sum":
            res = data.resample(frequency, on=on).sum()
        elif aggregation_fct == "mean":
            res = data.resample(frequency, on=on).mean()
        elif aggregation_fct == "max":
            res = data.resample(frequency, on=on).max()
        elif aggregation_fct == "min":
            res = data.resample(frequency, on=on).min()
        elif aggregation_fct == "asfreq":  # Upsampling option
            res = data.resample(frequency, on=on).asfreq()
        elif aggregation_fct == "ffill":
            res = data.resample(frequency, on=on).ffill()
        elif aggregation_fct == "bfill":
            res = data.resample(frequency, on=on).bfill()
        else:
            raise Exception("Error: unsupported aggregation function.")

        return {"output_data": res}
