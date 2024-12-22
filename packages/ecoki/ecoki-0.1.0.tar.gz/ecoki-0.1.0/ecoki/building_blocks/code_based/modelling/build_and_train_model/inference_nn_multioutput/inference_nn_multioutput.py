from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd
import pickle
from sklearn.multioutput import MultiOutputRegressor
from keras.models import Sequential, Model
from keras.layers import Input, LSTM, Dense, Concatenate, Dropout, Masking, Flatten, TimeDistributed
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler, StandardScaler

class InferenceNNMultioutput(BuildingBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "ecoKI"
        self.description = "Dieser Baustein kann die Inferenz für ein trainiertes neuronales Netz (Regressor) bereitstellen. Zuvor muss dieses mit der Pipeline Train_Neural_Network_Multi erstellt worden sein, welches dann auch direkt diesen Baustein definiert und eine entsprechende Custom-Inferenz-Pipeline erstellt."
        self.version = "1"
        self.category = "Modeling"

        self.add_inlet_port('input_data', object)
        self.add_outlet_port('output_data', object)

        # flag indicating wether the model was already loaded
        self.model_loaded = False

    # predict
    def predict(self, features):
        # Make predictions
        features_scaled = self.feature_scaler.transform(features.loc[:,self.settings["feature_names"]])
        y_pred_scaled = self.model.predict(features_scaled)
        y_pred = self.label_scaler.inverse_transform(y_pred_scaled)
        return pd.DataFrame(columns=self.settings["label_names"], data=y_pred)

    def execute(self, input_data):

        if not self.model_loaded:

            self.model = load_model(self.settings["model_file_path"])
            self.feature_scaler = pickle.load(open(self.settings["feature_scaler_file_path"], 'rb'))
            self.label_scaler = pickle.load(open(self.settings["label_scaler_file_path"], 'rb'))
            self.model_loaded = True

        # get predictions
        predictions = self.predict(input_data)

        return {"output_data": predictions}