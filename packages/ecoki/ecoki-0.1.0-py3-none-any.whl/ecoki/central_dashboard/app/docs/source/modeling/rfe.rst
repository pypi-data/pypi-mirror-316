RecursiveFeatureElimination
===========================

This module provides functionality for performing Recursive Feature Elimination (RFE) with Cross-Validation. It is designed as part of the EcoKI architecture and is implemented as a building block for feature selection in machine learning pipelines.

The main component of this module is the `RecursiveFeatureElimination` class, which encapsulates the process of:

1. Performing feature selection using Recursive Feature Elimination with Cross-Validation.
2. Supporting both classification and regression tasks.
3. Providing flexibility in choosing the estimator for feature selection.
4. Ranking features based on their importance.
5. Outputting selected features and their rankings.

This module is particularly useful for identifying the most relevant features in a dataset, which can improve model performance and interpretability.

Key features of this module include:
- Seamless integration with the EcoKI building block framework.
- Support for various estimators including SVC, DecisionTreeClassifier, RandomForestClassifier, and XGBClassifier.
- Flexibility in setting the minimum number of features to select.
- Comprehensive output including feature rankings and selected features.

The module leverages scikit-learn's RFECV and RFE implementations, making it a powerful tool for feature selection in the EcoKI ecosystem.

Parameters
-----------

.. autoclass:: ecoki.building_blocks.code_based.modelling.build_and_train_model.recursive_feature_elimination.recursive_feature_elimination.RecursiveFeatureElimination
   :members:

Example
-------

Here's a basic example of how to use the :class:`RecursiveFeatureElimination` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.modelling.build_and_train_model.recursive_feature_elimination.recursive_feature_elimination import RecursiveFeatureElimination

   # Initialize the building block
   rfe = RecursiveFeatureElimination()

   # Configure the settings
   rfe.settings = {
       "selected_columns_label": ["target"],
       "selected_columns": ["feature1", "feature2", "feature3"],
       "selectEstimator": ["RandomForestClassifier"],
       "min_features_to_select": 2
   }

   # Assuming you have your data prepared
   input_data = prepare_your_data()

   # Execute the feature selection process
   result = rfe.execute(input_data)

   # Access the results
   feature_rankings = result['output_data']
   selected_features = result['output_data_1']
   additional_data = result['output_data_2']

.. seealso::
   :class:`sklearn.feature_selection.RFECV`
   :class:`sklearn.feature_selection.RFE`

