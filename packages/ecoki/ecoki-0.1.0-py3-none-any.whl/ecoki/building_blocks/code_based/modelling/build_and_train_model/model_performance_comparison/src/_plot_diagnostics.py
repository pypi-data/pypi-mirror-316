import os
import matplotlib 
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns # plotting library
from sklearn.model_selection import learning_curve
import xgboost
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import save_plot
from sklearn.linear_model import LinearRegression
import math
import pandas as pd
import dataframe_image as dfi
import itertools
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class PlotDiagnostics:

    def _plot_settings(self, train_sizes, train_scores_mean, validation_scores_mean, name):
        # plt.figure()
        plt.style.use('seaborn-v0_8')
        sns.set_theme(style="whitegrid")
        plt.plot(train_sizes, train_scores_mean, label = 'Training error')
        plt.plot(train_sizes, validation_scores_mean, label = 'Validation error')
        plt.ylabel('MAE', fontsize = 12)
        plt.xlabel('Training Set Size', fontsize = 12)
        title = "{}".format(name)
        plt.title(title, fontsize = 14, y = 1.03)
        plt.legend(loc='upper right', borderaxespad=0, frameon=True)
        plt.xlim(0)
        # plt.ylim((0,0.1))

    def plot_learning_curve (self, ml_model):
        # Plot learning curves for given estimator. 
        # name: string type, name of the estimator that will be shown in plot title
        # estimator: object type, that implements the “fit” and “predict” methods
        # X: dataframe of the features
        # Y: dataframe of the labels
    
        # Tutorial: https://www.dataquest.io/blog/learning-curves-machine-learning/
    
        # Set the training data sizes that will be plotted in the learning curves
        max_size = math.floor(self.X.shape[0]*0.8) # max size of data set is that of the full training data set. NOTE, this assumes that a 5-fold CV will be used 
        training_sizes = [10,math.floor(max_size*0.2),math.floor(max_size*0.40),math.floor(max_size*0.6),math.floor(max_size*0.80),max_size]
        
        self.estimator = ml_model
        ## Learning curves are relatively straightforward; Only following three lines needed to create learning curve data
        # Learning curve for given estimator
        train_sizes, train_scores, validation_scores = learning_curve(
        estimator = self.estimator, X = self.X, y = self.Y, train_sizes = training_sizes, cv = 5,
        scoring = 'neg_mean_absolute_error', shuffle = True, random_state=0)
    
        train_scores_mean = -train_scores.mean(axis = 1)
        validation_scores_mean = -validation_scores.mean(axis = 1)
        print('Mean training scores\n\n', pd.Series(train_scores_mean, index = train_sizes))
        print('\nMean validation scores\n\n',pd.Series(validation_scores_mean, index = train_sizes))
        print('\n', '-' * 20) # separator
        return [train_sizes, train_scores_mean, validation_scores_mean]        
        #self._plot_settings(train_sizes, train_scores_mean, validation_scores_mean, name)
        
    #def plot_NN_learning_curve(self, learning_curve_all_scores):
    #    train_sizes = learning_curve_all_scores['Training Set Size']
    #    train_scores_mean = learning_curve_all_scores['Training Error']
    #    validation_scores_mean = learning_curve_all_scores['Validation Error']
    #    name = "Conv. Neural Network"
    #    self._plot_settings(train_sizes, train_scores_mean, validation_scores_mean, "Conv. Neural Network")
        
    def plot_scores(self, df, num_features_label, savedir_path, y_limit):
    #def plot_scores(self, df, num_features, y_limit):
    
        # Plot a comparison of all the algorithms
        plt.figure()
        sns.set_theme(style="whitegrid")
        plot_data =df.copy().round({'Coeff. of Determination':2, 'Root Mean Square Error':3, 'Mean Absolute Error':3, 'Mean Absolute % Error':3})
        plot_data.columns=['Algorithm','$R^2$/10','RMSE','MAE','MAPE']
        plot_data.drop(columns=['MAPE'],inplace=True) # MAPE metric is not needed in plot
        plot_data['$R^2$/10'] = plot_data['$R^2$/10']/10 # Scale for improved readability
        fig, ax1 = plt.subplots(figsize=(8, 4))
        plt.title(num_features_label, fontsize=16)
        tidy = plot_data.melt(id_vars='Algorithm').rename(columns=str.title)

        chart = sns.barplot(x="Algorithm", y="Value", hue='Variable', data=tidy, ax=ax1)
        chart.set_xlabel("Algorithm", fontsize=14)
        chart.set_ylabel("Value", fontsize=14)
        chart.set_xticklabels(chart.get_xticklabels(), rotation=0, horizontalalignment='center')
        chart.set(ylim=(0, y_limit+0.02))
        plt.legend(bbox_to_anchor=(1.05, 1.05), loc='upper left', borderaxespad=0)
        sns.despine(fig)
    
        for i in chart.containers:
            chart.bar_label(i,rotation=0)
        plot_name = "Performance Comparison.png"
    
        import textwrap
        def wrap_labels(ax, width, break_long_words=False):
            labels = []
            for label in ax.get_xticklabels():
                text = label.get_text()
                labels.append(textwrap.fill(text, width=width,
                              break_long_words=break_long_words))
            ax.set_xticklabels(labels, rotation=0)
    
        wrap_labels(ax1, 14)
        ax1.figure
        
        img_path = save_plot(os.path.join(savedir_path, 'figures', num_features_label), "%s"%(plot_name))
        plt.close()
        return img_path
        #save_plot(os.path.join(results_identifier, 'results', 'figures', "%s features"%(num_features)), "%s"%(plot_name))
        #plot_fig = plt.gcf()
        #plot_fig.set_size_inches(17, 8)
        #return plot_fig
        #return plt.gcf()

    # dont call it for now. Comment it. Maybe have for MVP but not for ecoki
    def plot_important_xgboost_features(self):
        plt.figure()
        sns.set_theme(style="whitegrid")
        fig, ax1 = plt.subplots(figsize=(10, 6))
        xgboost.plot_importance(self.model, max_num_features=15,
                                title='XGBoost Feature Importance', 
                                xlabel='F score', ylabel='Top 15 Features',
                                ax=ax1,height=0.4)
        plot_name = "XGBoost Feature Importance"
        # save_plot(analysis_name,plot_name)

    def plot_all_learning_curves(self, savedir_path, num_features_label, learning_curve_all_scores, y_lim):
        plots = []
        ylimit = (0, y_lim)
        num_subplots = len(learning_curve_all_scores)
        # Plot learning curves
        fig, axes = plt.subplots(1, num_subplots, figsize=(17,6))
        fig.suptitle(num_features_label, fontsize=16)
        plt.sca(axes[0])
        #self.estimator = LinearRegression()
        plots.append(self._plot_settings(learning_curve_all_scores[0][0], learning_curve_all_scores[0][1], learning_curve_all_scores[0][2], "Linear Regression"))
        plt.ylim(ylimit)
        plt.sca(axes[1])
        #self.estimator = xgboost.XGBRegressor()
        plots.append(self._plot_settings(learning_curve_all_scores[1][0], learning_curve_all_scores[1][1], learning_curve_all_scores[1][2], "XGBoost Regression"))
        plt.ylim(ylimit)
        if len(learning_curve_all_scores) > 2:
            plt.sca(axes[2])
            plots.append(self._plot_settings(learning_curve_all_scores[2]['Training Set Size'], learning_curve_all_scores[2]['Training Error'], learning_curve_all_scores[2]['Validation Error'], "Conv. Neural Network"))
            plt.ylim(ylimit)
        
        plot_name = "Learning Curves.png"
        img_path = save_plot(os.path.join(savedir_path, 'figures', num_features_label), "%s"%(plot_name))
        plt.close()
        return img_path        
        #return plt.gcf()
        
    def concat_plots(self, savedir_path, all_plots, plot_name):
        images = [Image.open(x) for x in all_plots]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths) + 40*(len(images)-1)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height), "WHITE")
        draw = ImageDraw.Draw(new_im)

        x_offset = 0
        x1, y1 = widths[0] + 20, 0
        x2, y2 = widths[0] + 20, heights[0]
        for ind, im in enumerate(images):
            new_im.paste(im, (x_offset,0))
            if ind == len(images)-1:
                continue
            endpoints = (x1, y1), (x2, heights[ind])
            draw.line(endpoints, fill=(0,0,0), width=3)
            x_offset += widths[ind] + 40
            x1 += widths[ind] + 40
            x2 += widths[ind] + 40

        storage_path = os.path.join(savedir_path, 'figures')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)      
        new_im.save(os.path.join(storage_path, "%s.png"%(plot_name)))
        return os.path.join(storage_path, "%s.png"%(plot_name))         

    def plot_model_prediction_performance(self, savedir_path, mae_values_all_analyses, num_features_selected_labels_list):
        num_cols = len(num_features_selected_labels_list)
        
        table_content = {"0":['Complex & Extensive ML', 'Simple & Quick ML', 'Simple & Quick Non-ML', '']}
        for ind, (num_feats_label, mae_values) in enumerate(zip(num_features_selected_labels_list, mae_values_all_analyses)):
            table_content[ind+1] = [mae_values[2], mae_values[1], mae_values[0], num_feats_label]
        
        df = pd.DataFrame(table_content)
        main_headers = []
        main_headers.append("")
        main_headers.extend(["Performance (MAE)"]*num_cols)
        df.columns = [main_headers, list(range(num_cols+1))]
        
        plot_name = "Model prediction performance summary (Mean Absolute Error)"
        styled_df = df.style.set_table_attributes("style='display:inline'").format(precision=3).hide(axis=0, level=0).hide(axis=1, level=1)
        styled_df.set_table_styles(
        [
            {"selector": "caption", "props": [("font-size", "150%"), ('font-weight', 'bold'), ('text-align','left'), ('margin-bottom', '20px')]},
            {"selector": "th", "props": [("border", "1px solid grey !important"), ('font-weight', 'bold'), ('text-align','center')]},
            {"selector": "tbody > tr:nth-child(even) > td", "props": [('text-align','center'), ('width', '1%'), ("white-space", "nowrap"), ("border", "1px solid grey !important"), ("background-color", "white")]},
            {"selector": "tbody > tr:nth-child(odd) > td", "props": [('text-align','center'), ('width', '1%'), ("white-space", "nowrap"), ("border", "1px solid grey !important"), ("background-color", "white")]},
            {"selector": "tr:last-child", "props": [('font-weight', 'bold')]},
            {"selector": "td:first-child", "props": [('width', '1%'), ('white-space', 'nowrap'), ('font-weight', 'bold')]},
        ], overwrite=False)
        
        storage_path = os.path.join(savedir_path, 'figures')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
        img_file_path = os.path.join(storage_path, "%s.png"%(plot_name))             
        dfi.export(styled_df, img_file_path)          

        df_csv = pd.DataFrame(table_content)
        df_csv.columns = [main_headers, list(range(num_cols+1))]        
        df_csv.columns = df_csv.columns.droplevel(1)
        storage_path = os.path.join(savedir_path, 'data')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path) 
        df_csv.to_csv(os.path.join(storage_path, "%s.csv"%(plot_name)), index=False)
        return img_file_path
        
    def outline_recommended_models(self, mae_values_list, noteworthiness_threshold, img_path):
        # rotate matrix
        mae_values_all = [[mae_values_list[j][i] for j in range(len(mae_values_list))] for i in range(len(mae_values_list[0])-1,-1,-1)]
        start_row = 1
        if any(mae=="" for mae_arr in mae_values_all for mae in mae_arr):    # if MAE was not computed for complex-ML
            mae_values_all[0] = [None]*len(mae_values_all[0])            # replace empty values with None
            start_row=2   # Donot consider first row as Complex-ML is not included
            mae_min = np.min(mae_values_all[1:])    # get minimum MAE
        else:
            mae_min = np.min(mae_values_all)         # get minimum MAE
        
        index_min_mae = np.argwhere(mae_values_all == mae_min)    # get table cell index(es) of minimum MAE (one or more cells could have mimimum error)
        all_non_noteworthy_cell_coords, all_num_steps = self.find_non_noteworthy_models(mae_values_all, index_min_mae, noteworthiness_threshold)  # get non-noteworthy table cells
        recommended_models_coords_list = self.find_best_models(all_non_noteworthy_cell_coords, all_num_steps, start_row)  # recommend best models
        
        img = Image.open(img_path)         # read image
        na = np.array(img)
        legend_arr = np.zeros([70, na.shape[1], 3], dtype = np.uint8)
        legend_arr[:, :] = [255, 255, 255]
        na = np.concatenate((na, legend_arr))
        table_row_indexes, table_col_indexes = self.find_rows_and_columns_coordinates(na) # Read coordinates of horizontal and vertical lines of the table in image for outlining best model(s) later
        td_rows = list(table_row_indexes[start_row:-1])  
        td_cols = table_col_indexes[1:]

        # coordinates for drawing recommended model legend, minimum MAE and noteworthiness threshold on image
        leg_start_x = table_col_indexes[0] + 20
        leg_start_y = table_row_indexes[-1] + 10
        leg_end_x = table_col_indexes[0] + 40
        leg_end_y = leg_start_y

        pil_im = Image.fromarray(na)
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype("arial.ttf", 12)
        # draw recommended model legend, minimum MAE and noteworthiness threshold on image
        draw.text((leg_start_x, leg_end_y+5),"Minimum Error = %s"%(mae_min),(0,0,0),font=font)
        draw.text((leg_start_x, leg_end_y+25),"Noteworthiness Threshold = %s"%(noteworthiness_threshold),(0,0,0),font=font)
        draw.rectangle(((leg_start_x,leg_start_y+45), (leg_start_x+10,leg_start_y+55)), width=3, outline="red")
        draw.text((leg_end_x, leg_end_y+45),"Recommended Model",(255,0,0),font=font)

        for i in range(len(td_rows)-1):
            for j, col_n in enumerate(td_cols):
                if j < len(td_cols)-1:
                    for coords in recommended_models_coords_list:
                        if i == coords[0] and j == coords[1]:
                            # outline borders of recommended model cell in the table
                            draw.rectangle(((td_cols[j], td_rows[i]), (td_cols[j+1], td_rows[i+1])), width=3, outline="red")
        pil_im.save(img_path)  # overwrite image file
        return img_path

    def find_non_noteworthy_models(self, mae_values_all, minimum_mae_index, noteworthiness_threshold):
        all_non_noteworthy_cell_coords = []  # shortlisted table cell coordinates for which the difference of MAE to Minimum MAE doesn't exceed noteworthiness threshold
        all_num_steps = []           # number of steps or table cells that the shortlisted cells are from the cell(s) with minimum MAE
        
        for min_val_index in minimum_mae_index:           # for each index of cell having minimum MAE
            shortlisted_mae_orig_coords_list = []
            num_steps_list = []
            row_ind = min_val_index[0]
            col_ind = min_val_index[1]
            mae_analysis_list = [row[0:col_ind+1] for row in mae_values_all[row_ind:]]
            num_rows = len(mae_analysis_list)
            num_cols = len(mae_analysis_list[0])
            min_val = mae_analysis_list[0][num_cols-1]

            for i in range(num_rows):
                for j in range (num_cols):
                    if i==0 and j==num_cols-1:
                        continue
                    diff = round(mae_analysis_list[i][j] - min_val, 3)      # calculate difference of minimum MAE cell with another cell
                    if diff < noteworthiness_threshold:                                 # if difference is less than noteworthiness threshold
                        shortlisted_mae_orig_coords_list.append((i+row_ind, j))  # shortlist cell coordinates
                        num_steps = i + (num_cols - 1 - j)                       # record number of steps to minimum MAE cell
                        num_steps_list.append(num_steps)
            if not shortlisted_mae_orig_coords_list:       # if all other cells have MAE difference greater than or equal to noteworthiness threshold
                shortlisted_mae_orig_coords_list.append((row_ind, col_ind))    # select mimimum MAE cell as recommended model
            all_non_noteworthy_cell_coords.append(shortlisted_mae_orig_coords_list)
            all_num_steps.append(num_steps_list)
        return all_non_noteworthy_cell_coords, all_num_steps

    def find_best_models(self, all_non_noteworthy_cell_coords, all_num_steps_list, start_row):
        recommended_models_coords_list = []
        for ind, num_steps_list in enumerate(all_num_steps_list):  # get number of steps recorded for all cells having MAE difference less than noteworthiness threshold
            if not num_steps_list:                            # if no steps recorded, all MAE differences are above threshold 
                coords = all_non_noteworthy_cell_coords[ind][0]       # therefore, select coordinates of mimimum MAE cell as recommended model
                recommended_model_row_ind = coords[0] - 1 if start_row == 2 else coords[0]
                recommended_model_col_ind = coords[1]
                recommended_models_coords_list.append((recommended_model_row_ind, recommended_model_col_ind))
            else:                                             # otherwise, consider cells having maximum number of steps as recommended models
                max_steps_index_list = np.argwhere(num_steps_list == np.max(num_steps_list))
                for i, max_step_index in enumerate(max_steps_index_list):
                    coords = all_non_noteworthy_cell_coords[ind][max_step_index[0]]
                    recommended_model_row_ind = coords[0] - 1 if start_row == 2 else coords[0]
                    recommended_model_col_ind = coords[1]
                    recommended_models_coords_list.append((recommended_model_row_ind, recommended_model_col_ind))
        return recommended_models_coords_list

    def find_rows_and_columns_coordinates(self, img_pixels):
        rows = [0]*img_pixels.shape[0]
        cols = [0]*img_pixels.shape[1]
        for x in range(img_pixels.shape[0]):
            for y in range(img_pixels.shape[1]):
                if list(img_pixels[x][y]) == [128, 128, 128]:
                    rows[x] = rows[x]+1
                    cols[y] = cols[y]+1
                    
        table_row_indexes = [idx for idx, val in enumerate(rows) if val > 0.9*img_pixels.shape[1]]  # get coordinates of table row borders in image  
        table_col_indexes = [idx for idx, val in enumerate(cols) if val > 0.3*img_pixels.shape[0]]  # get coordinates of table column borders in image
        return table_row_indexes, table_col_indexes