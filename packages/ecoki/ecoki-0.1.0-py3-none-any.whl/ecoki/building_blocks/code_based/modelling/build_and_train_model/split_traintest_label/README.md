`<b><u>`Module: SplitTrainTestLabel `</u></b>`

This module, part of the EcoKI architecture, is designed to split a pre-processed input dataset into training and testing datasets. This splitting is crucial for model training and evaluation in machine learning pipelines.

## Short description

Splitting Dataset into Training and Testing Sets

The `SplitTrainTestLabel` class, a `BuildingBlock` in the EcoKI architecture, facilitates the division of an input dataset into distinct training and testing sets. The class allows a 10% split of the original dataset size for testing. This split helps in training models on a large portion of the dataset while setting aside a smaller section for model evaluation and prediction accuracy testing.

## Inputs

### Necessary:

- "input_data": A pandas DataFrame object that contains the pre-processed input data.

### Optional:

- "selected_columns_label": Specifies the label column in the DataFrame for supervised learning tasks.
- "selected_columns": Specifies the feature columns to be included in the analysis.

## Exits

In case of exceptions during the dataset splitting process, the module logs appropriate errors for debugging and troubleshooting.

### Expected results:

The output of this module is a dictionary containing:

1. The training dataset (x_train).
2. The testing dataset (x_valid).
3. The training labels (y_train).
4. The testing labels (y_valid).
5. The label column name or names.

### Output format:

The output is formatted as a list containing the respective pandas DataFrame objects for training and testing datasets and their labels.

## Parameters

The module allows setting parameters for label columns and selected columns, facilitating a customizable approach to dataset splitting based on the user's requirements.

## History

1.0.0 -> Initial release
