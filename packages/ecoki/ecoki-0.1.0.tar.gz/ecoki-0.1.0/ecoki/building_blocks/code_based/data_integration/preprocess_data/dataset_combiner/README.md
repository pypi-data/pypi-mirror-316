<b><u>Module: DatasetCombiner</u></b>

This module combines multiple pandas dataframes into one. 

######

## Short description

The DatasetCombiner combines the given list of dataframes into one dataframe.

The axis on which to combine the dataframe can be specified using the "axis" parameter.
If "0" rows are considered, if "1" columns are considered.

The type of join to use can be specified using the "join" parameter.
If "outer", the intersection of the specified axis is calculated. If "inner", the union of the specified axis is calculated.

Whether to ignore original indices or not can be specified using the "ignore_index" parameter.
If True, the original indices are dropped and the new dataframe is indexed 0...n-1.

## Inputs
### Necessary:
- "input_data": A list of pandas dataframes.

### Optional:
none

## Exits
In case of any exceptions during parameter checking or combining, None is returned and a status code of 1 is set on the output port.

### Expected results:
The output of this building block is a dataframe containing data from all given dataframes depending on the specified axis, join and ignore_index parameters.

### Output format:
The output format is a pandas DataFrame.

## Parameters
"axis": The axis on which to combine the dataframes. Choice between "0" and "1". Default values is "0".
"join": Type of join that should be used. Choice between "inner" and "outer". Default value is "outer".
"ignore_index": Specifies whether to ignore the indices in the original dataframes. Choice between "True" and "False". Default value is "False".

## History
1.0.0 -> Initial release