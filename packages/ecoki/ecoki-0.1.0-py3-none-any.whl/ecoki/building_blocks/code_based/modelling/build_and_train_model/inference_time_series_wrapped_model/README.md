<b><u>Module: InferenceNNMultioutput </u></b>

Dieser Baustein kann eine bestehende Inferenz-Pipeline mit den vorgenommenen Transformationen durch Aggregatsfunktionen auf den Feature ausführen. Zuvor müssen diese Aggregatsfunktionen im Baustein TimeSeriesWrapper definiert worden sein, der auch eine Inferenzpipeline mit diesem Baustein startet.

######

## Short description

Dieser Baustein kann eine bestehende Inferenz-Pipeline mit den vorgenommenen Transformationen durch Aggregatsfunktionen auf den Feature ausführen. Zuvor müssen diese Aggregatsfunktionen im Baustein TimeSeriesWrapper definiert worden sein, der auch eine Inferenzpipeline mit diesem Baustein startet.
## Inputs
### Necessary:
- "input_data": A pandas DataFrame containing the (wrapped) features

### Optional:
none

## Exits

### Expected results:
- "output_data": A pandas DataFrame containing the (wrapped) predictions
- "unwrapped_output_data": A pandas DataFrame containing the unwrapped predictions that came from the underlying inference model
- "unwrapped_input_data": A pandas DataFrame containing the unwrapped features that were used to call the underlying inference model

### Output format:
The output format is a pandas DataFrame.

## Parameters

## History
1.0.0 -> Initial release