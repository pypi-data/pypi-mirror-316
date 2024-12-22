<b><u>Module: SplitTrainTest</u></b>

This module is responsible for splitting the input dataset (pre-processed) into train and test datasets (20% size of the original) for further training and prediction tasks.

######

## Short description

Split Train and Test datasets

The `SplitTrainTest` class, derived from the `BuildingBlock` class, receives an input dataset, resets its index, identifies labels, and splits it into train and test datasets using the sklearn's `train_test_split` function. The ratio for the split is 80:20 (train:test). The output is a list of four datasets - x_train, x_valid, y_train, y_valid.

## inputs
### Necessary:
- "input_data": A pandas DataFrame object that is preprocessed and ready to be split into training and test datasets.

### Optional:
none

## exits
In case of any exceptions during the split operation, an empty list is returned and a status code of 1 is set on the output port.

### Expected results:
The output of this module is a list of four datasets - x_train, x_valid, y_train, y_valid. 

### Output format:
The output format is a list of pandas DataFrame objects.

## parameters
The following parameters should be set in the settings.json file:
- "label_column": Specifies the column(s) in the dataframe that act as the label/target for training the machine learning model.

## History
1.0.0 -> Initial release
