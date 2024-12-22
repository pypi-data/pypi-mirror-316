from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd
import pickle
import xgboost as xgb
from sklearn.multioutput import MultiOutputRegressor

class InferenceXgboostMultioutput(BuildingBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "ecoKI"
        self.description = "Dieser Baustein kann die Inferenz für einen XGBoostRegressor bereitstellen. Zuvor muss dieses mit der Pipeline Train_Xgboost_Multi erstellt worden sein, welches dann auch direkt diesen Baustein definiert und eine entsprechende Custom-Inferenz-Pipeline erstellt."

        self.version = "1"
        self.category = "Modeling"

        self.add_inlet_port('input_data', object)
        self.add_outlet_port('output_data', object)

        # flag indicating wether the model was already loaded
        self.model_loaded = False

    def load_model(self,filename):

        # Create the XGBoost regressor model
        self.xgb_regressor = xgb.XGBRegressor()

        # Create the multi-output regressor model using XGBoost
        self.multi_output_regressor = MultiOutputRegressor(self.xgb_regressor)
        self.multi_output_regressor = pickle.load(open(filename, 'rb'))

        return self.multi_output_regressor

    # predict
    def predict(self, features):
        # Make predictions
        y_pred = self.model.predict(features)
        return pd.DataFrame(columns=self.settings["label_names"], data=y_pred)

    def execute(self, input_data):

        if not self.model_loaded:

            self.model = self.load_model(self.settings["model_file_path"])
            self.model_loaded = True

        # save inference features as csv? -> not in this version
        #self.test_features.to_csv('test_features.csv')

        # get predictions
        predictions = self.predict(input_data)

        return {"output_data": predictions}