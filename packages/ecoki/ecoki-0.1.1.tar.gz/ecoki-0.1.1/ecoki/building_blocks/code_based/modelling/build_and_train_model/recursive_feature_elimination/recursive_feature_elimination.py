from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd
import numpy as np

# sklearn imports
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV, RFE
import xgboost as xgb

class RecursiveFeatureElimination(BuildingBlock):
    """Perform Recursive Feature Elimination with Cross-Validation.

    This class is designed to perform feature selection by recursively removing features and building a model 
    with the remaining features. It uses cross-validation to determine the optimal number of features to maximize 
    the performance of a given estimator.

    Attributes:
        architecture: The name of the architecture (EcoKI).
        description: A brief description of the class.
        version: The version number of the class.
        category: The category of the class (Transformer).
        input_data: The input data for the feature selection.
        output_data: The output data containing the feature rankings.
        output_data_1: The output data containing the selected features.
        output_data_2: Additional output data.
    """

    def __init__(self, **kwargs):
        """Initializes the RecursiveFeatureElimination class with specified keyword arguments.

        Args:
            **kwargs: Keyword arguments for the BuildingBlock superclass.
        """
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Perform Recursive Feature Elimination with Cross-Validation"
        self.version = "1"
        self.category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', pd.DataFrame)
        self.add_outlet_port('output_data_1', object)
        self.add_outlet_port('output_data_2', pd.DataFrame)

    def execute(self, input_data):
        """Executes the feature selection process using Recursive Feature Elimination with Cross-Validation.

        Args:
            input_data: The input data frame containing features and labels for the feature selection process.

        Returns:
            A dictionary containing the output data frames with feature rankings, the selected features, and additional data.
        """
        # Get the input data
        labels_global = self.settings["selected_columns_label"]
        features_global = self.settings["selected_columns"]
        selectEstimator = self.settings["selectEstimator"][0]
        # min_features_to_select = self.settings["min_features_to_select"]
        dataset = input_data

        def rfecv_classification(X, y, min_features_to_select=1, selectEstimator='SVC'):
            """Performs Recursive Feature Elimination with Cross-Validation for classification tasks.

            Args:
                X: Feature matrix.
                y: Target variable.
                min_features_to_select: Minimum number of features to select.
                selectEstimator: Name of the estimator to use.

            Returns:
                A tuple containing the selector object and a DataFrame with feature rankings.
            """
            if selectEstimator == 'SVC':
                targetEstimator = SVC(kernel="linear")
            elif selectEstimator == 'DecisionTreeClassifier':
                targetEstimator = DecisionTreeClassifier()
            elif selectEstimator == 'GradientBoostingClassifier':
                targetEstimator = GradientBoostingClassifier()
            elif selectEstimator == 'RandomForestClassifier':
                targetEstimator = RandomForestClassifier()
            elif selectEstimator == 'XGBClassifier':
                targetEstimator = xgb.XGBClassifier()

            rfecv = RFECV(
                estimator=targetEstimator,
                step=1,
                cv=StratifiedKFold(2),
                scoring="accuracy",
                min_features_to_select=min_features_to_select)
            selector = rfecv.fit(X, y)

            feature_cols = pd.Series(np.arange(X.shape[1]))
            feature_support = pd.Series(rfecv.support_)
            feature_ranking = pd.Series(rfecv.ranking_)

            frame = {'feature': feature_cols, 'feature_selected': feature_support, 'ranking': feature_ranking}
            rfe_df = pd.DataFrame(frame).sort_values('feature', ascending=True)

            return selector, rfe_df

        def rfe_classification(X, y, n_features_to_select=1, selectEstimator='SVR'):
            """Performs Recursive Feature Elimination for classification tasks.

            Args:
                X: Feature matrix.
                y: Target variable.
                n_features_to_select: Number of features to select.
                selectEstimator: Name of the estimator to use.

            Returns:
                A tuple containing the selector object and a DataFrame with feature rankings.
            """
            if selectEstimator == 'SVC':
                targetEstimator = SVC(kernel="linear")
            elif selectEstimator == 'DecisionTreeClassifier':
                targetEstimator = DecisionTreeClassifier()
            elif selectEstimator == 'GradientBoostingClassifier':
                targetEstimator = GradientBoostingClassifier()
            elif selectEstimator == 'RandomForestClassifier':
                targetEstimator = RandomForestClassifier()
            elif selectEstimator == 'XGBClassifier':
                targetEstimator = xgb.XGBClassifier()

            rfe = RFE(
                estimator=targetEstimator,
                step=1,
                n_features_to_select=1)
            selector = rfe.fit(X, y)

            feature_cols = X.columns
            feature_support = pd.Series(rfe.support_)
            feature_ranking = pd.Series(rfe.ranking_)

            frame = {'feature': feature_cols, 'feature_selected': feature_support, 'ranking': feature_ranking}
            rfe_df = pd.DataFrame(frame)

            return selector, rfe_df

        def rfecv_regression(X, y, min_features_to_select=1, selectEstimator='SVR'):
            """Performs Recursive Feature Elimination with Cross-Validation for regression tasks.

            Args:
                X: Feature matrix.
                y: Target variable.
                min_features_to_select: Minimum number of features to select.
                selectEstimator: Name of the estimator to use.

            Returns:
                A tuple containing the selector object and a DataFrame with feature rankings.
            """
            if selectEstimator == 'SVR':
                targetEstimator = SVR(kernel="linear")
            elif selectEstimator == 'DecisionTreeRegressor':
                targetEstimator = DecisionTreeRegressor()
            elif selectEstimator == 'RandomForestRegressor':
                targetEstimator = RandomForestRegressor()
            elif selectEstimator == 'XGBRegressor':
                targetEstimator = xgb.XGBRegressor()
            elif selectEstimator == 'GradientBoostingRegressor':
                targetEstimator = GradientBoostingRegressor()

            rfecv = RFECV(
                estimator=targetEstimator,
                step=1,
                cv=5,
                min_features_to_select=min_features_to_select)
            selector = rfecv.fit(X, y)

            feature_cols = X.columns 
            feature_support = pd.Series(rfecv.support_)
            feature_ranking = pd.Series(rfecv.ranking_)

            frame = {'feature': feature_cols, 'feature_selected': feature_support, 'ranking': feature_ranking}
            rfe_df = pd.DataFrame(frame)

            return selector, rfe_df

        def rfe_regression(X, y, n_features_to_select=1, selectEstimator='SVR'):
            """Performs Recursive Feature Elimination for regression tasks.

            Args:
                X: Feature matrix.
                y: Target variable.
                n_features_to_select: Number of features to select.
                selectEstimator: Name of the estimator to use.

            Returns:
                A tuple containing the selector object and a DataFrame with feature rankings.
            """
            if selectEstimator == 'SVR':
                targetEstimator = SVR(kernel="linear")
            elif selectEstimator == 'DecisionTreeRegressor':
                targetEstimator = DecisionTreeRegressor()
            elif selectEstimator == 'RandomForestRegressor':
                targetEstimator = RandomForestRegressor()
            elif selectEstimator == 'XGBRegressor':
                targetEstimator = xgb.XGBRegressor()
            elif selectEstimator == 'GradientBoostingRegressor':
                targetEstimator = GradientBoostingRegressor()

            rfe = RFE(
                estimator=targetEstimator,
                step=1,
                n_features_to_select=1)
            selector = rfe.fit(X, y)

            feature_cols = X.columns
            feature_support = pd.Series(rfe.support_)
            feature_ranking = pd.Series(rfe.ranking_)

            frame = {'feature': feature_cols, 'feature_selected': feature_support, 'ranking': feature_ranking}
            rfe_df = pd.DataFrame(frame)

            return selector, rfe_df

        # Get the features and labels
        X = dataset[features_global]
        y = dataset[labels_global]

        # Call the RFECV function and process the result
        if selectEstimator in ['SVC', 'DecisionTreeClassifier', 'RandomForestClassifier', 'XGBClassifier']:
            rfecv_tuple = rfecv_classification(X=X, y=y, min_features_to_select=1, selectEstimator=selectEstimator)
            rfe_tuple = rfe_classification(X=X, y=y, n_features_to_select=1, selectEstimator=selectEstimator)
        else:
            rfecv_tuple = rfecv_regression(X=X, y=y, min_features_to_select=1, selectEstimator=selectEstimator)
            rfe_tuple = rfe_regression(X=X, y=y, n_features_to_select=1, selectEstimator=selectEstimator)
        rfe_result = rfecv_tuple[1]
        rfe_result_sort = rfe_result.sort_values('ranking', ascending=False)
        ranking_bar = rfe_result['ranking'].to_list()
        feature_bar = rfe_result['feature'].astype(str).to_list()
        support_bar = rfe_result['feature_selected'].astype(str).to_list()
        data_bar = {
            'Feature ranking':ranking_bar,
            'Feature':feature_bar,
            #'Feature selected':support_bar
        }

        # Feature ranking
        ranking_funnel = rfe_result_sort['ranking'].to_list()
        feature_funnel = rfe_result_sort['feature'].astype(str).to_list()
        support_funnel = rfe_result_sort['feature_selected'].astype(str).to_list()
        data_funnel = {
            'Feature ranking':ranking_funnel,
            'Feature':feature_funnel,
            'Feature selected':support_funnel
        }

        # Create the output data
        df = pd.DataFrame(data=data_bar["Feature ranking"], index=data_bar["Feature"],
                        columns=["Feature_rank"]).sort_values(by="Feature_rank", ascending=False)

        # Repeat above for feature ranking from RFE function (note that the selector from RFE is not needed, as we are only interested in the ranked list)
        rfe_result = rfe_tuple[1]
        rfe_result_sort = rfe_result.sort_values('ranking', ascending=False)
        ranking_bar = rfe_result['ranking'].to_list()
        feature_bar = rfe_result['feature'].astype(str).to_list()
        support_bar = rfe_result['feature_selected'].astype(str).to_list()
        data_bar = {
            'Feature ranking': ranking_bar,
            'Feature': feature_bar,
            # 'Feature selected':support_bar
        }

        # Feature ranking
        ranking_funnel = rfe_result_sort['ranking'].to_list()
        feature_funnel = rfe_result_sort['feature'].astype(str).to_list()
        support_funnel = rfe_result_sort['feature_selected'].astype(str).to_list()
        data_funnel = {
            'Feature ranking': ranking_funnel,
            'Feature': feature_funnel,
            'Feature selected': support_funnel
        }

        # Create the output data
        df_full_rank = pd.DataFrame(data=data_bar["Feature ranking"], index=data_bar["Feature"],
                            columns=["Feature_rank"]).sort_values(by="Feature_rank", ascending=True)

        return {"output_data": df, "output_data_1": rfecv_tuple[0], "output_data_2": df_full_rank}
