<b><u>Building block: Optimierung 2D-Visualisierung</u></b>

Dieser Baustein zeigt einen interaktiven 2D-Plot, der für die zu optimierenden Parameter die Vorhersage des Modells für die Labels und das Rating angibt
######

## Brief Description

Optimierung 2D-Visualisierung

Dieser Baustein zeigt einen interaktiven 2D-Plot, der für die zu optimierenden Parameter die Vorhersage des Modells für die Labels und das Rating angibt. Auf diese Weise kann dem Nutzer geholfen werden, die Entscheidung des Optimierers zur Anpassung der Prozessparameter nachzuvollziehen. Auf die X- und Y-Achse des Plots können die zu optimierenden Prozessparameter gesetzt werden. Bei mehr als zwei Prozessparametern können somit unterschiedliche 2D-Kombinationen erzeugt werden. Über 'Output_Name' kann das Label des Modells gewählt werden, für das der Nutzer eine farblich gekennzeichnete Kontur geplottet haben möchte. Hier stehen alle Ausgänge des Modells sowie das Rating des Optimierers entstanden durch die Optimierungsfunktion zur Auswahl. Über den 'Testdaten_Index' kann das Sample des Testdatensatzes ausgewählt werden, für das der Plot erstellt wird. Außerdem sind sowohl die originale Parameterkombination des Testdatensatzes (gelb) als auch der optimierte Parametervorschlag (rot) dargestellt. Außerdem ist es möglich, über den Button 'Zeige_Trainingsdatensatz_Kombinationen' alle vorkommenden Parameterkombinationen des Trainingsdatensatzes anzuzeigen. Denn der Optimierer schlägt nur neue Kombinationen vor, die sich in direkter Nähe zu einer festgelegten Mindestzahl an bekannten Kombinationen befindet. So kann nachvollzogen werden, warum nicht aussichtsreichere Parameterkombinationen im 2D-Raum vorgeschlagen wurden.

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
no parameters to be set in settings.json

## Version history
0.0.1 -> Initial release 