from ecoki.building_block_framework.building_block import BuildingBlock
from matplotlib import pyplot
import numpy as np
import typing
from math import sqrt
from numpy import array
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, LSTM, RepeatVector, TimeDistributed

class ModelAndForecast(BuildingBlock):
    """Building block for LSTM model building, training and making predictions on the test dataset.

    This class extends the BuildingBlock class to create an LSTM model, train it on the provided
    training data, and make predictions on the test dataset.

    Attributes:
        architecture (str): The name of the architecture (EcoKI).
        description (str): A brief description of the building block's functionality.
        version (str): The version of the building block.
        category (str): The category of the building block (Transformer).
    """

    def __init__(self, **kwargs):
        """Initialize the ModelAndForecast building block.

        Args:
            **kwargs: Additional keyword arguments to be passed to the parent BuildingBlock class.
        """
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.description = "Builds the LSTM model, trains it on the training set and makes predictions on the testing set"
        self.version = "1"
        self.category = "Transformer"
        self.add_inlet_port('input_data', list)
        self.add_inlet_port('data_sequences_timesteps', list)
        self.add_inlet_port('target_column', dict)
        self.add_outlet_port('test_and_forecasted_data', list)
        self.add_outlet_port('sequences_timesteps', list)
        self.add_outlet_port('target', dict)
    
    def build_model(self, train_x, train_y):
        """Build and train the LSTM model.

        Args:
            train_x (numpy.ndarray): The input features for training.
            train_y (numpy.ndarray): The target values for training.

        Returns:
            keras.models.Sequential: The trained LSTM model.
        """
        # define parameters
        n_timesteps, n_features, n_outputs = train_x.shape[1], train_x.shape[2], train_y.shape[1]
        print(n_outputs)
        # reshape output into [samples, timesteps, features]
        train_y = train_y.reshape((train_y.shape[0], train_y.shape[1], 1))
        print(train_y.shape)
        # define model
        model = Sequential()
        if self.settings['nn_complexity'] == 'Basic':
            model.add(LSTM(50, activation='relu', input_shape=(n_timesteps, n_features)))
            #model.add(RepeatVector(n_outputs))
            #model.add(LSTM(200, activation='relu', return_sequences=True))
            #model.add(TimeDistributed(Dense(100, activation='relu')))
            #model.add(TimeDistributed(Dense(1)))
            model.add(Dense(25, activation='relu'))
            model.add(Dense(n_outputs))
            model.compile(loss='mse', optimizer='adam')
            # fit network
            hist = model.fit(train_x, train_y, epochs=20, batch_size=6, verbose=1)
        print("Training Done!!!...")
        return model

    def forecast(self, model, test_x):
        """Make predictions using the trained model.

        Args:
            model (keras.models.Sequential): The trained LSTM model.
            test_x (numpy.ndarray): The input features for testing.

        Returns:
            numpy.ndarray: The predicted values.
        """
        y_h = model.predict(test_x, verbose=0)
        print("Forecasting Done!!!...")
        return y_h
    
    def execute(self, input_data, data_sequences_timesteps, target_column):
        """Execute the model building, training, and forecasting process.

        Args:
            input_data (list): A list containing training and testing data.
            data_sequences_timesteps (list): Sequence and timestep information.
            target_column (dict): Information about the target column.

        Returns:
            dict: A dictionary containing the test and forecasted data, sequences timesteps, and target information.
        """
        output_data_port = self.get_port('test_and_forecasted_data', 'outlet')

        x_train, y_train, x_test, y_test = input_data
        model = self.build_model(x_train, y_train)
        y_h = self.forecast(model, x_test)
        print(x_test.shape, y_test.shape, y_h.shape)

        test_and_forecasted_data = [x_test, y_test, y_h]
        return {"test_and_forecasted_data": test_and_forecasted_data,
                "sequences_timesteps": data_sequences_timesteps,
                "target": target_column}
