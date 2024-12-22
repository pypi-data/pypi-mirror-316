from ecoki.visualizer_framework.visualizer import Visualizer
import hvplot.pandas
import panel as pn
from panel.interact import interact, fixed
import pandas as pd

pn.extension()


# plotting fuction
def plot_lstm_model_predictions(samples, timesteps, target_column, target_input_legend, target_output_legend, 
                                target_prediction_legend, xlabel, ylabel, TestSample_Index=0):
                                      
    x_test, y_test, y_h = samples
    x_i = list(x_test[TestSample_Index][:,int(next(iter(target_column)))]) + [None]*len(y_test[TestSample_Index])         
    y_i = [None]*len(x_test[TestSample_Index]) + list(y_test[TestSample_Index])
    y_h_i = [None]*len(x_test[TestSample_Index]) + list(y_h[TestSample_Index])                
    # Create a DataFrame with timesteps as index
    df = pd.DataFrame({target_input_legend: x_i,
                       target_output_legend: y_i,
                       target_prediction_legend: y_h_i}, index=timesteps[TestSample_Index])

    # Use hvplot to create a HoloViews plot
    plot = df.hvplot.line(y=(target_input_legend, target_output_legend, target_prediction_legend), 
                          xlabel=xlabel, rot=90, ylabel=ylabel)
    return plot


class PredictionsVisualizer(Visualizer):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.app = None

    def run(self):
        self.terminate()

        data_sequences_timesteps = self.input_dict["timesteps"][0]
        target_col = self.input_dict["target"]
        test_and_forecasted_data = self.input_dict["input_data"]
        target_ip_legend = "Target input"
        target_op_legend = "Target output"
        target_pred_legend = "Target prediction"
        x_label = "Time"
        y_label = next(iter(target_col.values()))
        
        # define the panel interact function
        layout = interact(plot_lstm_model_predictions,
                          TestSample_Index=(0, len(test_and_forecasted_data[0])-1, 1),
                          samples=fixed(test_and_forecasted_data),
                          timesteps=fixed(data_sequences_timesteps),
                          target_column=fixed(target_col),
                          target_input_legend=fixed(target_ip_legend),
                          target_output_legend=fixed(target_op_legend),
                          target_prediction_legend=fixed(target_pred_legend),
                          xlabel=fixed(x_label),
                          ylabel=fixed(y_label))

        # Display the plot using Panel
        self.app = pn.Column('# LSTM Model Predictions', pn.Row(layout[0], layout[1])).servable().show(open=False, threaded=True, 
                                                                           port=self.port, websocket_origin=f'127.0.0.1:{self.port}')

    def terminate(self):
        if self.app:
            self.app.stop()
