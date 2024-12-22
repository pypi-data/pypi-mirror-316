from ecoki.visualizer_framework.visualizer import Visualizer

import panel as pn
import hvplot.pandas
import panel as pn
from panel.interact import interact, fixed

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


pn.extension()

# plotting fuction
def plot_optimisation_ranges_2D(samples, optimized_data, model, col_names, Output_Name, X_Parameter, Y_Parameter,
                                X_Left, X_Right, Y_Left, Y_Right, optim_settings,
                                process_parameter_names, training_samples=None, dim1_grid_number=100,
                                dim2_grid_number=100,Zeige_Trainingsdatensatz_Parameterkombinationen=False,Testdaten_Index=1):
    """
    Plots the 2D optimization ranges for the given parameters.

    This function creates a 2D plot to visualize the optimization ranges for the specified parameters.
    It helps in understanding the decision-making process of the optimization algorithm by showing
    the model predictions for labels and ratings based on optimized parameters.

    Args:
        samples (tuple): A tuple containing training and test samples.
        optimized_data (pd.DataFrame): The optimized data.
        model (object): The model used for predictions.
        col_names (list): List of column names.
        Output_Name (str): The name of the output label to be plotted.
        X_Parameter (str): The name of the parameter to be plotted on the X-axis.
        Y_Parameter (str): The name of the parameter to be plotted on the Y-axis.
        X_Left (float): The left bound for the X-axis parameter.
        X_Right (float): The right bound for the X-axis parameter.
        Y_Left (float): The left bound for the Y-axis parameter.
        Y_Right (float): The right bound for the Y-axis parameter.
        optim_settings (dict): The optimization settings.
        process_parameter_names (list): List of process parameter names.
        training_samples (pd.DataFrame, optional): The training samples. Defaults to None.
        dim1_grid_number (int, optional): The number of grid points for the X-axis. Defaults to 100.
        dim2_grid_number (int, optional): The number of grid points for the Y-axis. Defaults to 100.
        Zeige_Trainingsdatensatz_Parameterkombinationen (bool, optional): Flag to show training dataset parameter combinations. Defaults to False.
        Testdaten_Index (int, optional): The index of the test data sample to be plotted. Defaults to 1.

    Returns:
        None
    """
    # adjust Index (1->n instead of 0->n-1)
    Testdaten_Index = Testdaten_Index-1

    sample = samples[1].iloc[[Testdaten_Index], :]
    optimized_sample = optimized_data.iloc[[Testdaten_Index], :]

    training_samples = samples[0]
    # for pid in samples.index:
    #
    #     optimisation_parameter_names = model_feature_structure.get_optimisation_parameter_names()
    #     optimisation_bounds_left = model_feature_structure.get_optimisation_bounds_left()
    #     optimisation_bounds_right = model_feature_structure.get_optimisation_bounds_right()
    #
    #     combs = combinations(range(len(optimisation_parameter_names)), 2)
    #
    #     for idx_pair in combs:

    # # get infos for dim1
    # dim1_name = optimisation_parameter_names[idx_pair[0]]
    # dim1_left_bound = optimisation_bounds_left[idx_pair[0]]
    # dim1_right_bound = optimisation_bounds_right[idx_pair[0]]
    #
    # # get infos for dim2
    # dim2_name = optimisation_parameter_names[idx_pair[1]]
    # dim2_left_bound = optimisation_bounds_left[idx_pair[1]]
    # dim2_right_bound = optimisation_bounds_right[idx_pair[1]]

    # get bounds
    x_left_bound = optim_settings['optimisation_parameters'][X_Parameter]["left_bound"]
    x_right_bound = optim_settings['optimisation_parameters'][X_Parameter]["right_bound"]
    x_resolution = optim_settings['optimisation_parameters'][X_Parameter]["resolution"]

    y_left_bound = optim_settings['optimisation_parameters'][Y_Parameter]["left_bound"]
    y_right_bound = optim_settings['optimisation_parameters'][Y_Parameter]["right_bound"]
    y_resolution = optim_settings['optimisation_parameters'][Y_Parameter]["resolution"]

    x_left_value = x_left_bound+(x_right_bound-x_left_bound)*X_Left
    x_right_value = x_left_bound + (x_right_bound - x_left_bound) * X_Right

    y_left_value = y_left_bound+(x_right_bound-y_left_bound)*Y_Left
    y_right_value = y_left_bound + (y_right_bound - y_left_bound) * Y_Right

    dim1_grid_number = int(np.round((x_right_bound-x_left_bound)/x_resolution)+1)
    dim2_grid_number = int(np.round((y_right_bound-y_left_bound)/y_resolution)+1)

    if dim1_grid_number>100:
        dim1_grid_number=100

    if dim2_grid_number > 100:
        dim2_grid_number = 100

    # create meshs
    dim1_space = np.linspace(x_left_value, x_right_value, dim1_grid_number)
    dim2_space = np.linspace(y_left_value, y_right_value, dim2_grid_number)
    dim1_grid, dim2_grid = np.meshgrid(dim1_space, dim2_space)

    sample_with_optimized_params = sample.copy()
    sample_with_optimized_params.loc[:,optim_settings['optimisation_parameters'].keys()] = optimized_sample.loc[:,[str(key)+"_optimized" for key in optim_settings['optimisation_parameters'].keys()]].values

    # duplicate sample and fill with grid values
    # grid_frame = pd.concat([samples.loc[[pid], :]] * len(dim1_grid) * len(dim2_grid))
    grid_frame = pd.DataFrame(pd.np.repeat(sample_with_optimized_params.values, dim1_grid.shape[0] * dim1_grid.shape[1], axis=0),
                              columns=sample_with_optimized_params.columns)
    grid_frame[X_Parameter] = dim1_grid.flatten()
    grid_frame[Y_Parameter] = dim2_grid.flatten()

    grid_prediction = model.predict(grid_frame)  # get_api_post_dataframe(model_predict_route, df=grid_frame, df_parameter_name="x")
    grid_rating = model.objective_function(grid_prediction,optim_settings)

    #
    # for column in grid_rating.columns:

    #fig, axs = plt.subplots(1, 3, gridspec_kw={'width_ratios': [10, 1, 10]}, figsize=(20, 25))
    fig, axs = plt.subplots(1,2, gridspec_kw={'width_ratios': [10, 1]}, figsize=(20, 25))
    # plt.title(str(pid) + ' auf ' + str(samples.loc[pid, 'Material']))
    im = axs[0].contourf(dim1_grid, dim2_grid,
                         grid_rating.loc[:, [Output_Name]].values.reshape((dim1_grid.shape[0], dim1_grid.shape[1])), 30,
                         cmap='viridis')
    axs[0].set_xlabel(X_Parameter)
    axs[0].set_ylabel(Y_Parameter)
    fig.colorbar(im, cax=axs[1], label=Output_Name)

    if Zeige_Trainingsdatensatz_Parameterkombinationen:
        if (not training_samples is None):
            axs[0].scatter(training_samples.loc[:, X_Parameter], training_samples.loc[:, Y_Parameter], c='black',
                           label='Alle vorkommenden Parameterkombinationen im Trainingsdatensatz',s=10)

    # # train artikel points circles
    # # axs[0].scatter(train_all.loc[train_all['Material']==features.loc[pid,'Material'],f1_name],train_all.loc[train_all['Material']==features.loc[pid,'Material'] ,f2_name], s=1000, facecolors='none', edgecolors='r')
    # [axs[0].add_artist(Ellipse((a, b), 0.1, 3, 0, facecolor='none', edgecolor='r')) for a, b in
    #  zip(train_all.loc[train_all['Material'] == features.loc[pid, 'Material'], f1_name],
    #      train_all.loc[train_all['Material'] == features.loc[pid, 'Material'], f2_name])]

    # train artikel points
    # axs[0].scatter(training_samples.loc[training_samples['Material'] == samples.loc[pid, 'Material'], dim1_name],
    #                training_samples.loc[training_samples['Material'] == samples.loc[pid, 'Material'], dim2_name], c='red',
    #                label=str('Alle Parameterkombinationen für Artikelnr ' + str(
    #                    samples.loc[pid, 'Material']) + ' im Trainingsdatensatz'))

    #sample_prediction = model.predict(sample, col_names)  # get_api_post_dataframe(model_predict_route, df=grid_frame, df_parameter_name="x")
    #sample_rating = model.objective_function(sample_prediction, optim_settings)

    # recipe points
    axs[0].scatter(sample.loc[:, X_Parameter], sample.loc[:, Y_Parameter], c='white', s=100 ,marker = 'x',
                   label=str('Originale Parameterkombination im Testdatensatz für Eintrag '+str(Testdaten_Index)+' ; Wert: '+str(optimized_sample.loc[:,Output_Name].iloc[0])))
    axs[0].scatter(optimized_sample.loc[:, str(X_Parameter+"_optimized")], optimized_sample.loc[:, str(Y_Parameter+"_optimized")], c='red', s=100,marker = 'x',
                   label=str('Optimierte Parameterkombination im Testdatensatz für Eintrag '+str(Testdaten_Index)+' ; Wert: '+str(optimized_sample.loc[:,str(Output_Name+'_optimized')].iloc[0])))


    axs[0].legend(fontsize=8)
    axs[0].set_xlim(x_left_value, x_right_value)
    axs[0].set_ylim(y_left_value, y_right_value)
    # axs[2].axis('tight')
    # axs[2].axis('off')
    display_features = list(process_parameter_names) + list(grid_rating.columns)

    # tab = axs[2].table(cellText=pd.DataFrame(data=[display_features,
    #                                                sample.round(2).loc[:,
    #                                                list(process_parameter_names)].values.astype(
    #                                                    str).tolist()]).transpose().values,
    #                    colWidths=[0.85, 0.15],
    #                    # rowLabels=X_features,
    #                    colLabels=['', "Index"],
    #                    # cellLoc = 'left', rowLoc = 'top',
    #                    loc='center',
    #                    fontsize=12
    #                    )
    # tab.auto_set_font_size(False)
    # # tab.set_fontsize(12)
    # tab.scale(1, 5)
    # axs[2].axis("off")

    # plt.subplots_adjust(right=0.1)
    fig = plt.gcf()
    #fig.set_size_inches(15, 8)
    fig.set_size_inches(9, 8)
    # fig.savefig(str(pid+'_'+y_labels[nr]+'_Parameterraum'+'_'+f1_name+'_'+f2_name+'.jpg'),dpi=500)

    return fig

class Optimization2DVisualizerVisualizer(Visualizer):
    """
    Optimization2DVisualizerVisualizer Class

    This class extends the Visualizer class and provides functionality for visualizing 2D optimization results.
    It includes methods for initializing the visualizer, making predictions, and calculating objective functions.

    Methods
    -------
    __init__(**kwargs)
        Initializes the Optimization2DVisualizerVisualizer instance with the provided keyword arguments.

    predict(features)
        Makes predictions using the inference pipeline and returns the predicted values as a DataFrame.

    objective_function(predictions, optimizer_settings, include_predictions=True, only_rating=False)
        Calculates the objective function based on the provided predictions and optimizer settings.

    Attributes
    ----------
    Inherits all attributes from the Visualizer class.
    """
    def __init__(self, **kwarg):
        """
        Initializes the Optimization2DVisualizerVisualizer instance.

        Args:
            **kwarg: Arbitrary keyword arguments.
        """
        super().__init__(**kwarg)

    # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
    # def predict(self, features,column_names):
    #     # Make predictions
    #     # y_pred = self.building_block.model.predict(features)
    #     y_pred = self.input_dict["input_data_settings"].predict(features)

    def predict(self, features):
        """
        Makes predictions using the inference pipeline and returns the predicted values as a DataFrame.

        Args:
            features (pd.DataFrame): The input features for making predictions.

        Returns:
            pd.DataFrame: A DataFrame containing the predicted values.
        """
        
        # prerequesite: inference pipeline needs to have been created already
        inner_loop_args = {
            "inputs": [
                {
                    "building_block": "Inference_BuildingBlock",
                    "inlet": "input_data",
                    "value": features
                }
            ],
            "outputs": [
                {
                    "building_block": "Inference_BuildingBlock",
                    "outlet": "output_data"
                }
            ]
        }

        y_pred = self.input_dict["pp_manager"].get_pipeline_executor(
            self.input_dict["input_data_settings"]['prediction_pipeline_name']).run_with_args(
            inner_loop_args, self.input_dict["pp_manager"])

        return pd.DataFrame(columns=list(self.input_dict["input_data_split_train_test"][2]), data=y_pred[0]['value'])


    # just a copy from the optimisation bb, should be replaced in the future
    # def objective_function(self, predictions, include_predictions=True, only_rating=False):
    #
    #     # define columns
    #     quality = predictions.loc[:, 'apple_juice_quality'].values
    #     energie = predictions.loc[:, 'energy_consumption_production'].values
    #
    #     # calculate costs
    #     predictions['Rating'] = np.where(quality < 4, (1 + 4 - quality) * energie,
    #                                      energie)
    #     return predictions

    def objective_function(self, predictions, optimizer_settings, include_predictions=True, only_rating=False):
        """
        Calculates the objective function for the given predictions.

        This function evaluates the objective function based on the provided predictions and optimizer settings.
        It computes the rating for each prediction by considering the optimization target and boundary conditions.

        Args:
            predictions (pd.DataFrame): The predicted values.
            optimizer_settings (dict): The settings for the optimizer, including the objective function and boundary conditions.
            include_predictions (bool, optional): Flag to include predictions in the output. Defaults to True.
            only_rating (bool, optional): Flag to return only the rating. Defaults to False.

        Returns:
            pd.DataFrame: A DataFrame containing the predictions and the calculated rating.
        """

        # set optimization target column
        minimization_value = predictions.loc[:, optimizer_settings['objective_function']['optimization_target']].values

        rating = minimization_value

        # iterate over boundary conditions
        for condition,condition_value in optimizer_settings['objective_function']['boundary_conditions'].items():

            if condition_value['operator'] == "greater":
                boundary_penalty_term = np.where(predictions.loc[:, condition_value['label_name']].values < condition_value['boundary'], 1 + condition_value['boundary'] - predictions.loc[:, condition_value['label_name']].values, 1)

            elif condition_value['operator'] == "smaller":
                boundary_penalty_term = np.where(predictions.loc[:, condition_value['label_name']].values > condition_value['boundary'], 1 + predictions.loc[:, condition_value['label_name']].values - condition_value['boundary'], 1)

            else:
                print("Optimization boundary operator not valid")
                continue

            # multiply
            rating = rating*boundary_penalty_term

        # set rating
        predictions['Rating'] = rating

        return predictions


    def run(self):
        """
        Runs the 2D optimization visualizer.

        This method initializes the visualizer, sets up the interactive plot, and starts the visualization
        process. It uses the input data, optimizer settings, and other parameters to create an interactive
        2D plot that helps users understand the decision-making process of the optimization algorithm.

        The method performs the following steps:
        1. Initializes the visualizer.
        2. Sets up the interactive plot using the `interact` function from the `panel` library.
        3. Starts the visualization process by creating a servable panel.

        Args:
            None

        Returns:
            None
        """
        self.terminate()

        split_train_test_list = self.input_dict["input_data_split_train_test"]
        optimized_data = self.input_dict["input_data"]
        col_names = list(self.input_dict["input_data_split_train_test"][2])
        optimizer_settings = self.input_dict["input_data_settings"]

        # define the panel interact function
        layout = interact(plot_optimisation_ranges_2D,
                          Testdaten_Index=(1, len(optimized_data), 1),
                          samples=fixed(split_train_test_list),model=fixed(self),
                          optimized_data=fixed(optimized_data),
                          col_names = fixed(col_names),
                          Output_Name=col_names+["Rating"],
                          X_Parameter=list(reversed([name for name in optimizer_settings['optimisation_parameters'].keys()])),
                          Y_Parameter=[name for name in optimizer_settings['optimisation_parameters'].keys()],
                          X_Left=fixed(0.0),#(0.0,1.00,0.01),
                          X_Right=fixed(1.0),#(0.0,1.00,0.01),
                          Y_Left=fixed(0.0),#(0.0,1.00,0.01),
                          Y_Right=fixed(1.0),#(0.0,1.00,0.01),
                          Zeige_Trainingsdatensatz_Parameterkombinationen = False,
                          optim_settings = fixed(optimizer_settings),
                          process_parameter_names=fixed([name for name in optimizer_settings['optimisation_parameters'].keys()]),
                          training_samples=fixed(None),
                          dim1_grid_number=fixed(50),
                          dim2_grid_number=fixed(50),
                          return_figures=fixed(False),
                          filepath=fixed('data/'),
                          sort_order=fixed(0))

        # start app
        #self.app = pn.Column('2D-Plot der Modellvorhersage zur Nachvollziehbarkeit der Optimierungsvorschläge', pn.Row(layout[0], layout[1])).servable().show(open=False, threaded=True, port=self.port,
        #                                        websocket_origin=f'127.0.0.1:{self.port}')
        self.visualizer = pn.Column('2D-Plot der Modellvorhersage zur Nachvollziehbarkeit der Optimierungsvorschläge', pn.Row(layout[0], layout[1])).servable()
        self._show_visualizer()
