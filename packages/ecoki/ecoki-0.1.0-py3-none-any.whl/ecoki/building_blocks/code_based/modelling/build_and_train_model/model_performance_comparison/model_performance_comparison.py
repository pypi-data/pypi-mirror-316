from ecoki.building_block_framework.building_block import BuildingBlock

# dependency import
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import run_model_comparison

import pandas as pd
import os


class ModelPerformanceComparison(BuildingBlock):
    """A building block for comparing the performance of various machine learning models.

    This class provides functionality to train, test, and compare different models,
    including non-ML, simple ML, and complex ML models. It can handle multiple labels,
    perform recursive feature elimination (RFE), and optionally include neural network
    models in the comparison.

    Attributes:
        architecture (str): The name of the architecture (EcoKI).
        description (str): A brief description of the building block's functionality.
        version (str): The version of the building block.
        category (str): The category of the building block (Transformer).

    Args:
        **kwargs: Additional keyword arguments to be passed to the parent BuildingBlock class.
    """

    def __init__(self, **kwargs):
        """Initialize the ModelPerformanceComparison building block.

        Args:
            **kwargs: Additional keyword arguments to be passed to the parent BuildingBlock class.
        """
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Building Block for training and testing non-ML, simple-ML and Complex-ML models and comparing their performance"
        self.version = "1"
        self.category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)        
        self.add_outlet_port('error_metrics_data', list)
        self.add_outlet_port('learning_curves_data', list)
        self.add_outlet_port('rfe_number_labels', list)
        self.add_outlet_port('noteworthiness_threshold', float)
        self.add_outlet_port('plots_save_dir', str)
        
    def execute(self, input_data):
        """Execute the model performance comparison.

        This method runs the model comparison using the provided input data and settings.
        It trains and tests various models, computes error metrics, generates learning curves,
        and performs recursive feature elimination if specified.

        Args:
            input_data (pd.DataFrame): The input data for model training and testing.

        Returns:
            dict: A dictionary containing the following keys:
                error_metrics_data (list): Error metrics for each model and label.
                learning_curves_data (list): Learning curve data for each model and label.
                rfe_number_labels (list): Results of recursive feature elimination.
                noteworthiness_threshold (float): The threshold for determining noteworthy results.
                plots_save_dir (str): The directory where plots are saved.

        """
        error_metrics_data, learning_curves_data, rfe_number_labels, noteworthiness_threshold = run_model_comparison(
                             self.settings['analysis_name'], self.settings['results_folder_name'], input_data, self.settings['labels_list'],
                             self.settings['numbers_list_rfe'], self.settings['savedir_path'], self.settings['include_neural_network'],
                             self.settings['neural_network_python_script_path'], self.settings['neural_network_requirements_txt_path'],
                             self.settings['plot_learning_curves'])

        return {"error_metrics_data": error_metrics_data,
                "learning_curves_data": learning_curves_data,
                "rfe_number_labels": rfe_number_labels,
                "noteworthiness_threshold": noteworthiness_threshold,
                "plots_save_dir": os.path.join(self.settings['savedir_path'], self.settings['analysis_name'], self.settings['results_folder_name'])}
