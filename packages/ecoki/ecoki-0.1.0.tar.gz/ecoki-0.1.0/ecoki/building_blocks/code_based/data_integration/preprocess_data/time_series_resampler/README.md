<b><u>Module: TimeSeriesResampler</u></b>

This module resamples a given dataframe containing time series data. 

######

## Short description

The TimeSeriesResampler resamples a given dataframe containing time series data.

The name of the column containing the time data can be specified using the "on" parameter.

The frequency of the resampling can be specified using the "frequency" parameter.
Frequency choice of "xT" and "xmin" stand for minutes.

The function to use for aggregation can be specified using the "aggregation_fct" parameter.


## Inputs
### Necessary:
- "input_data": A pandas dataframe containing time-series data.

### Optional:
none

## Exits
In case of any exceptions during parameter checking or resampling, None is returned and a status code of 1 is set on the output port.

### Expected results:
The output of this building block is a dataframe containing resampled data from the input dataframe depending on the given column, frequency and aggregation function parameters.

### Output format:
The output format is a pandas DataFrame.

## Parameters
"on": The name of the column containing time information. Default value is "None". 
"frequency": The frequency with which to resample the data. Choice between "xT", "xmin", "H", "D", "W", "M" and "Y". Default value is "W".
"aggregation_fct": The function to use to aggregate the data in the specified sample interval. Choice between "sum", "mean", "max", "min", "asfeq", "ffill" and "bfill". Default value is "sum".

## History
1.0.0 -> Initial release