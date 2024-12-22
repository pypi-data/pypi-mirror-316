from ecoki.visualizer_framework.visualizer import Visualizer
import panel as pn
from panel.interact import interact, fixed
import pandas as pd
from bokeh.models.widgets.tables import StringFormatter, NumberFormatter
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import PlotDiagnostics

pn.extension('tabulator')


# plotting fuction
def concat_plots_and_adjust_image_size(plots, numbers_for_rfe_labels, savedir, plots_title, Image_Size=600):
                          
    plot_diagnostics = PlotDiagnostics()
    plots_row = pn.Row()
    plots_row.append(pn.pane.PNG(plot_diagnostics.concat_plots(savedir, plots, plots_title), width=Image_Size*len(numbers_for_rfe_labels)))
    return plots_row

def get_ylim_for_plots(df, prev_y_lim):
    df_rounded = df[['Coeff. of Determination', 'Root Mean Square Error', 'Mean Absolute Error']].copy().round({'Coeff. of Determination':2, 'Root Mean Square Error':3, 'Mean Absolute Error':3})
    df_rounded['Coeff. of Determination'] = df_rounded['Coeff. of Determination']/10
    df_max_col_wise = list(df_rounded.max())
    df_max_col_wise.append(prev_y_lim)
    return(max(df_max_col_wise))

class ModelPerformanceComparisonVisualizer(Visualizer):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def run(self):
        self.terminate()

        error_metrics_data = self.input_dict['error_metrics']
        
        mae_values_all_analyses = []
        y_lim = 0
        prev_y_lim = 0
        for err_metric in error_metrics_data:
            mae_values = [round(mae,3) for mae in list(err_metric['Mean Absolute Error'])[1:]]
            if len(err_metric)==3:
                mae_values.append("")
            mae_values_all_analyses.append(mae_values)
            
            y_lim = get_ylim_for_plots(err_metric, prev_y_lim)
            prev_y_lim = y_lim

        learning_curves_data = self.input_dict['learning_curves']
        num_features_labels = self.input_dict['rfe_number_labels']
        nw_threshold = self.input_dict['noteworthiness_threshold']
        plots_save_dir = self.input_dict['plots_save_dir']

        plot_diagnostics = PlotDiagnostics()

        #predict_perform_table_plot = pn.pane.PNG(plot_diagnostics.plot_model_prediction_performance(
        #                                                 savedir_path, analysis_name, results_folder_name, mae_values_all_analyses, num_features_labels
        #                                             ), width=200*len(rfe_num_list) if len(rfe_num_list)> 1 else 400)
        num_features_rfe = len(num_features_labels)
        predict_perform_table_img = plot_diagnostics.plot_model_prediction_performance(plots_save_dir, mae_values_all_analyses, num_features_labels)
        if num_features_rfe <= 3:
            image_with_model_recommendation = plot_diagnostics.outline_recommended_models(mae_values_all_analyses, nw_threshold, predict_perform_table_img)
       
        bokeh_formatters = {}
        predict_perform_table_content = {"Model Category":['Complex & Extensive ML', 'Simple & Quick ML', 'Simple & Quick Non-ML']}
        bokeh_formatters['Model Category'] = StringFormatter(font_style='bold')
        for (num_feats_label, mae_vals) in zip(num_features_labels, mae_values_all_analyses):
            if not mae_vals[2]:
                mae_vals[2] = None
            col_name = "MAE (%s)"%(num_feats_label)
            #bokeh_formatters[col_name] = NumberFormatter(format='0.000')
            predict_perform_table_content[col_name] = [mae_vals[2], mae_vals[1], mae_vals[0]]
        
        performance_summary = None
        predict_perform_table_df = pd.DataFrame(predict_perform_table_content)
        if num_features_rfe > 3:
            performance_summary = pn.widgets.Tabulator(predict_perform_table_df, show_index=False, text_align='center', formatters=bokeh_formatters)
        else:
            performance_summary = pn.Tabs()
            model_recommendation_image = pn.pane.PNG(image_with_model_recommendation, width=500)
            performance_summary.append(("Model Recommendation", model_recommendation_image))
            predict_perform_table_plot = pn.widgets.Tabulator(predict_perform_table_df, show_index=False, text_align='center', formatters=bokeh_formatters)
            performance_summary.append(("Mean Absolute Errors", predict_perform_table_plot))
        
        concat_plots_list = []
        plots = []
        score_plots_title = "Performance Comparison"
        for data in zip(num_features_labels, error_metrics_data):
            # Plot comparison of the scores
            plots.append(plot_diagnostics.plot_scores(data[1], data[0], plots_save_dir, y_lim))
        concat_plots_list.append([score_plots_title, plots])
 
        plots = []
        lc_plots_title = "Learning Curves Comparison"
        if learning_curves_data:
            for data in zip(num_features_labels, learning_curves_data):
                plots.append(plot_diagnostics.plot_all_learning_curves(plots_save_dir, data[0], data[1], 0.16))
            concat_plots_list.append([lc_plots_title, plots])        
        
        plots_in_tabs = pn.Tabs()
        for plots_title, plots_to_concat in concat_plots_list:
            # define the panel interact function for adjusting image size of concatenated plots
            concat_plots_interactive = interact(concat_plots_and_adjust_image_size,
                                                Image_Size=(600, 1400, 200),
                                                plots=fixed(plots_to_concat),
                                                numbers_for_rfe_labels=fixed(num_features_labels),
                                                savedir=fixed(plots_save_dir),
                                                plots_title=fixed(plots_title))        
            plots_in_tabs.append((plots_title, concat_plots_interactive))

        print("------------------ All plots created! -----------------------")
        print("------------------ Program completed! -----------------------")
        #pn.panel(plots, sizing_mode="stretch_width")

        # Display the plot using Panel
        self.visualizer = pn.Column("# Model prediction performance summary (Mean Absolute Error)", performance_summary, 
                                    "# Model prediction performance details", plots_in_tabs).servable()
        self._show_visualizer()
