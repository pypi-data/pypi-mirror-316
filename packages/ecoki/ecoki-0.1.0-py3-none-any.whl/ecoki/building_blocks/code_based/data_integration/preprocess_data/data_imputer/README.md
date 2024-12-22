<b><u>Module: DataImputer</u></b>

This module fills in missing values in tabular data. 

######

## Short description

The DataImputer fills any missing values in a given dataframe based on the available data and chosen imputing strategy.

The imputing strategy to be used can be specified using the "strategy_num" and "strategy_cat" parameters for numerical and categorial data respectively.

Which value to use for the "constant" imputing strategy can be specified using the "fill_value" parameter.

Which columns to exclude from imputation can be specified using the "labels" parameter.

## Inputs
### Necessary:
- "input_data": A pandas dataframe.

### Optional:
none

## Exits
In case of any exceptions during imputing or parameter processing, None is returned and a status code of 1 is set on the output port.

### Expected results:
The output of this building block is a dataframe with all missing values in the specified columns (or all columns if none are specified) filled with sensible data.

### Output format:
The output format is a pandas DataFrame.

## Parameters
"strategy_num": Imputing strategy to apply for numeric data. Choice between "mean", "median", "most_frequent" or "constant". Default value is "median".
"strategy_cat": Imputing strategy to apply for categorical data. Choice between "most_frequent" and "constant". Default value is "most_frequent".
"fill_value": Used to fill any missing values with the "constant" imputing strategy. Default value is None.
"labels": List containing the names of columns to exclude from imputation. Default value is None.

## History
1.0.0 -> Initial release