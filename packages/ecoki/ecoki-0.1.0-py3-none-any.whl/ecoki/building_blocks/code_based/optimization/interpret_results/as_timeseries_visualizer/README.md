<b><u>Building block: As Time Series Visualizer </u></b>

Dieser Baustein kann Features, die Zeitreihen darstellen (Beispiel: f1_T-1, ... , f1_T-10) anhand eines vorgegebenen Patterns (regular expression) identifizieren sowie visualisieren.
######

## Brief Description

As Time Series Visualizer

Dieser Baustein kann Features, die Zeitreihen darstellen (Beispiel: f1_T-1, ... , f1_T-10) anhand eines vorgegebenen Patterns (regular expression) identifizieren sowie visualisieren.

## Inputs
### Required: 
- 'input_data': Pandas DataFrame object with output_data from the 'ProcessParamaterOptimizer' building block
- 'input_data_split_train_test': List of 4 Pandas Dataframes that correspnd to the 'output_data' of the Building Block 'SplitTrainTestLabel'
- 'input_data_settings': JSON-structure that correspnds to the settings of building block 'ProcessParameterOptimizer'

### Optional: 
None

## Ouputs
None

### Expected Results: 
Interactive panel dashboard on the central dashboard
### Output Format:
Html/Panel Application running as a visualizer

## Parameters
RegEx pattern to be set

## Version history
0.0.1 -> Initial release 