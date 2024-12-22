<b><u>Module: DuplicatesRemover</u></b>

This module removes duplicate data in a given dataframe. 

######

## Short description

The DuplicatesRemover removes any duplicates in the given dataframe.

Duplicate columns with the same name and/or values are removed first. Then, duplicate rows are removed based on the given parameters.

The subset of columns to be used for duplicate checking can be specified using the "subset" parameter.

Whether to keep the first, last or none of the duplicate rows can be specified using the "keep" parameter. 
If "first" or "last" the first or last duplicate is kept respectively. If "False" is selected all duplicates are dropped.

## Inputs
### Necessary:
- "input_data": A pandas dataframe.

### Optional:
none

## Exits
In case of any exceptions during parameter checking or duplicate removal, None is returned and a status code of 1 is set on the output port.

### Expected results:
The output of this building block is a dataframe with duplicate columns and rows removed depending on the specified subset and keeping parameters.

### Output format:
The output format is a pandas DataFrame.

## Parameters
"subset": List of column names to use for duplication checking. Default value is None.
"keep": Specifies whether to keep any of the duplicates. Choice between "first", "last" and "False". Default value is "first".

## History
1.0.0 -> Initial release