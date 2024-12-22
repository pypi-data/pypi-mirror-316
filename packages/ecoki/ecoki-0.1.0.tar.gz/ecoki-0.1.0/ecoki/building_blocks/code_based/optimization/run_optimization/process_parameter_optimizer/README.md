<b><u>Building block: Process Parameter Optimizer</u></b>

Dieser Baustein führt eine Black-Box-Optimierung auf Basis eines maschinell erlernten Modells durch

######

## Brief Description

Optimierung 2D-Visualisierung

Dieser Baustein führt eine Black-Box-Optimierung auf Basis eines maschinell erlernten Modells durch. Die Optimierungsfunktion wird basierend auf den Augangs-Labels des verwendeten Modells definiert. Alle Einstellungen können in den Pipeline-Settings vorgenommen werden. Bei diesem Baustein handelt es sich um eine statische Analyse. Dabei wird für die ersten 100 Beispiele des Trainingsdatensatzes jeweils eine Optimierung der festgelegten Prozessparameter innerhalb definierter Grenzen vorgenommen. Als Ergebnis sind in folgender Visualisierung sowohl die originalen als auch die optimierten ('_optimized') Prozessparameter aufgelistet. Außerdem sind für beide Fälle die Vorhersagen des Modells für die Ausgangslabels dargestellt. Zuletzt ist auch das Rating-verfügbar, nach dem der Black-Box-Optimierer die Optimierung der Prozessparameter vorgenommen hat. In der Visualisierung können sowohl die Werte geplotte werden als auch unter 'Descriptive Statistics' die KPIs wie beispielsweise der Mittelwert der optimierten Labels eingesehen und verglichen weren."
        
## Inputs
### Required: 
- 'input_data' List of 4 Pandas Dataframes that correspnd to the 'output_data' of the Building Block 'SplitTrainTestLabel'
### Optional: 
None

## Ouputs

- 'output_data': Pandas DataFrame object containing process parameters, label prediction and rating both for the both optimized and non optimized test set
- 'output_data_split_train_test': List of 4 Pandas Dataframes that correspnd to the 'output_data' of the Building Block 'SplitTrainTestLabel'
- 'output_data_settings': JSON-structure that correspnds to the settings of building block 'ProcessParameterOptimizer'

### Expected Results: 
Interactive panel dashboard on the central dashboard launched by a visalizer and optimized test dataset (see 'output_data')
### Output Format:
Html/Panel Application running as a visualizer

## Parameters
no parameters to be set in settings.json

## Version history
0.0.1 -> Initial release 