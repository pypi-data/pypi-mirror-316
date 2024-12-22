import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree

class BIKScaledBallTree(object):

    def __init__(self, train_data,confidence_radius_names,confidence_radius_values , leaf_size):
        '''
           Init

           :param pd.Dataframe train_data: train data for the ball tree
           :param list margins: margins used for scaling the data before applying the BallTree fitting where the radius in all dimensions i 1
           :param int leaf_size: leaf size (see documentation for BallTree)
           :return: nothing

        '''

        # set params
        #self.model_feature_structure = model_feature_structure
        self.train_data = train_data
        self.train_data_scaled = None
        self.tree = None
        self.leaf_size = leaf_size

        self.confidence_radius_names = confidence_radius_names
        self.confidence_radius_values = confidence_radius_values
        self.margins_red = pd.Series(index=self.confidence_radius_names,data=self.confidence_radius_values)

        # scale the train data and create the Ball tree
        self.margin_scale()
        self.tree = BallTree(self.train_data_scaled, self.leaf_size)

    def valid_key(self, data):
        return True

    def margin_scale(self):
        self.train_data_scaled = self.train_data.loc[:, self.confidence_radius_names]

        self.train_data_scaled = self.train_data_scaled.divide(self.margins_red)

        return

    def get_near_combinations(self, data):
        data_red = data.loc[:, self.confidence_radius_names]

        data_red = data_red.divide(self.margins_red)

        return self.tree.query_radius(data_red, r=1, count_only=True)

    def get_near_radius(self, data, neighbours):
        data_red = data.loc[:, self.confidence_radius_names]

        data_red = data_red.divide(self.margins_red)

        return self.tree.query(data_red, k=neighbours)

    def get_near_combinations_single(self, data):
        data_red = data.loc[:, self.confidence_radius_names]

        data_red = data_red.divide(self.margins_red)

        return self.tree.query_radius(data_red.values.reshape(1, -1), r=1, count_only=True)

    def get_near_radius_single(self, data, neighbours):
        data_red = data.loc[:, self.confidence_radius_names]

        data_red = data_red.divide(self.margins_red)

        return self.tree.query(data_red.values.reshape(1, -1), k=neighbours)
