<b><u>Module: InferenceNNMultioutput </u></b>

Dieser Baustein kann die Inferenz für ein trainiertes neuronales Netz (Regressor) bereitstellen. Zuvor muss dieses mit der Pipeline Train_Neural_Network_Multi erstellt worden sein, welches dann auch direkt diesen Baustein definiert und eine entsprechende Custom-Inferenz-Pipeline erstellt.

######

## Short description

Dieser Baustein kann die Inferenz für ein trainiertes neuronales Netz (Regressor) bereitstellen. Zuvor muss dieses mit der Pipeline Train_Neural_Network_Multi erstellt worden sein, welches dann auch direkt diesen Baustein definiert und eine entsprechende Custom-Inferenz-Pipeline erstellt.

## Inputs
### Necessary:
- "input_data": A pandas DataFrame containing the features

### Optional:
none

## Exits

### Expected results:
A pandas DataFrame containing the predictions

### Output format:
The output format is a pandas DataFrame.

## Parameters

## History
1.0.0 -> Initial release