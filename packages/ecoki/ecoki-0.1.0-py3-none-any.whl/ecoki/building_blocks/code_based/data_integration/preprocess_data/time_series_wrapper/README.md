<b><u>Module: Time Series Wrapper</u></b>

Dieser Baustein kann eine Zeitreihe zusammenfassen und sie zu einem Merkmal aggregieren. Dabei kann das MAXIMUM, der DURCHSCHNITT oder der MEDIAN als Aggregatsfunktion für jede Gruppierung spezifiziert werden. Auf diese Weise können Zeitreihen beispielsweise für die Nutzung im Optimierungsbaustein vorbereitet werden, sodass sie nur durch einen Wert charakterisiert werden kann. Außerdem wird eine Infereenz-Pipeline gestartet werden, die eine bestehende Inferenz-Pipeline mit den definierten Transformationen der Daten ausführen kann.

######

## Short description

This function block can summarize a time series and aggregate it into a characteristic. The MAXIMUM, the AVERAGE or the MEDIAN can be specified as an aggregate function for each grouping. In this way, time series can be prepared for use in the optimization module, for example, so that they can be characterized by just one value.

## Inputs
### Necessary:
- "input_data": A list of pandas DataFrames. The list should contain four elements in the following order: x_train, x_test, y_train, y_test.

### Optional:
none

## Exits

### Expected results:
A list of pandas DataFrames

### Output format:
- "output": A list of pandas DataFrames. The list should contain four elements in the following order: x_train, x_test, y_train, y_test. In this output the aggregated features are replaced by the aggregation.

## History
1.0.0 -> Initial release