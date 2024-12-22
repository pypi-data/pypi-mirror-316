<b><u>Module: RecursiveFeatureElimination</u></b>

The RecursiveFeatureElimination module is designed to perform feature selection using Recursive Feature Elimination combined with cross-validation. This process helps in identifying the most significant features for a given machine learning model, whether it's for regression or classification tasks.

######

## Short description

Feature Selection with Recursive Feature Elimination (RFE)

The `RecursiveFeatureElimination` class, part of the `BuildingBlock` suite, implements a method to select the most relevant features for training machine learning models. It does so by recursively considering smaller and smaller sets of features, using a variety of estimators such as SVC, DecisionTree, RandomForest, XGBoost, GradientBoosting for both classification and regression. The class uses cross-validation (StratifiedKFold for classification and regular KFold for regression) to enhance the robustness of the feature selection process. This method is particularly useful in reducing overfitting and improving model performance by eliminating irrelevant or redundant features.\
The `sklearn.feature_selection.RFECV` and `sklearn.feature_selection.RFE()` modules are used.

Links to documentation: [RFECV](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFECV.html), [RFE](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE)

Since the documentation does not explain how RFECV selects features, here is a explanation from stackoverflow:


>Your guess (edited out now) thinks of an algorithm that cross-validates the elimination step itself, but that is not how RFECV works. (Indeed, such an algorithm might stabilize RFE itself, but it wouldn't inform about the optimal number of features, and that is the goal of RFECV.)
> 
>Instead, RFECV runs separate RFEs on each of the training folds, down to min_features_to_select. These are very likely to result in different orders of elimination and final features, but none of that is taken into consideration: only the scores of the resulting models, for each number of features, on the test fold is retained. (Note that RFECV has a scorer parameter that RFE lacks.) Those scores are then averaged, and the best score corresponds to the chosen n_features_. Finally, a last RFE is run on the entire dataset with that target number of features.
>
> [source](https://stackoverflow.com/a/65557483)

## Inputs
### Necessary:
- "input_data": A pandas DataFrame where features are in columns and each row is an observation.

### Optional:
- "selected_columns_label": Specifies the label column in the DataFrame for supervised learning tasks.
- "selected_columns": Specifies the feature columns to be included in the analysis.
- "selectEstimator": A choice of estimator for assessing feature importance.

## Exits
In case of exceptions during the feature selection process, appropriate error handling should be implemented to handle such scenarios gracefully.

### Expected results:
The output of this module includes two parts:
1. A pandas DataFrame with features ranked based on their importance.
2. An object containing the fitted recursive feature elimination model.

### Output format:
1. DataFrame with feature rankings.
2. Model object (type depending on the chosen estimator).

## Parameters
The module allows setting parameters like the choice of estimator, the minimum number of features to select, and the columns to be considered for feature selection and labels.

## History
1.0.0 -> Initial release