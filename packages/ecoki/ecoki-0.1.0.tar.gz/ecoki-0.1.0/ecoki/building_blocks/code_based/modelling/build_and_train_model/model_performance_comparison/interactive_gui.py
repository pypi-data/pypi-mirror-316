# System imports
import pandas as pd
import panel as pn
import threading
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
import io
import os

pn.config.notifications = True
#pn.extension(sizing_mode="stretch_width")


class InteractiveGUI(AbstractInteractiveGUI):
    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.inputs_name = ["input_data"]
        self.buttons_dict = {}

    def create_labels_confirm_button(self):
        def labels_confirm(event):
            labels_list = self.labels_input.value
            print(labels_list)
            if labels_list:
                self.settings['labels_list'] = labels_list
                self.buttons_dict['labels_confirm_button'].disabled = True
                self.labels_input.disabled = True
                self.buttons_dict['numbers_for_rfe_confirm_button'].disabled = False
                self.numbers_for_rfe_input.disabled = False
                num_ip_features = len(self.input_data.columns.tolist()) - len(labels_list)
                self.numbers_for_rfe_input.options = list(range(1, num_ip_features+1))

        self.buttons_dict['labels_confirm_button'] = pn.widgets.Button(name='Confirm configuration', button_type='primary', margin=20,
                                                       width=100, align=('center'))
        self.buttons_dict['labels_confirm_button'].on_click(labels_confirm)

    def create_numbers_for_rfe_confirm_button(self):
        def numbers_for_rfe_confirm(event):
            numbers_list_rfe = self.numbers_for_rfe_input.value
            if numbers_list_rfe:
                self.settings['numbers_list_rfe'] = numbers_list_rfe
                self.numbers_for_rfe_input.disabled = True
                self.buttons_dict['numbers_for_rfe_confirm_button'].disabled = True
        
        self.buttons_dict['numbers_for_rfe_confirm_button'] = pn.widgets.Button(name='Confirm configuration', button_type='primary', margin=20,
                                                       width=100, align=('center'), disabled=True)
        self.buttons_dict['numbers_for_rfe_confirm_button'].on_click(numbers_for_rfe_confirm)
        
    def create_save_dir_confirm_button(self):
        def save_dir_confirm(event):
            analysis_name = self.analysis_name_input.value.strip()
            results_folder_name = self.results_name_input.value.strip()
            savedir_path = self.storage_path_input.value
            if True in (not analysis_name, not results_folder_name, not savedir_path) or len(savedir_path)>1:
                pass
            else:
                self.settings['analysis_name'] = analysis_name
                self.settings['results_folder_name'] = results_folder_name
                self.settings['savedir_path'] = savedir_path[0]
                self.analysis_name_input.disabled = True
                self.results_name_input.disabled = True
                #self.storage_path_input.disabled = True
                self.buttons_dict['save_dir_confirm_button'].disabled = True
        
        self.buttons_dict['save_dir_confirm_button'] = pn.widgets.Button(name='Confirm configuration', button_type='primary', margin=20,
                                                       width=100, align=('start'))
        self.buttons_dict['save_dir_confirm_button'].on_click(save_dir_confirm) 

    def create_generate_lc_confirm_button(self):
        def generate_lc_confirm(event):
            self.settings['plot_learning_curves'] = self.generate_learning_curve_cb.value
            self.generate_learning_curve_cb.disabled = True
            self.buttons_dict['generate_lc_confirm_button'].disabled = True
        
        self.buttons_dict['generate_lc_confirm_button'] = pn.widgets.Button(name='Confirm configuration', button_type='primary', margin=20,
                                                       width=100, align=('center'))
        self.buttons_dict['generate_lc_confirm_button'].on_click(generate_lc_confirm) 

    def create_include_nn_confirm_button(self):
        def include_nn_confirm(event):
            include_neural_network = self.include_neural_network_cb.value
            self.settings['include_neural_network'] = include_neural_network
            self.include_neural_network_cb.disabled = True
            self.buttons_dict['include_nn_confirm_button'].disabled = True
            
            def neural_network_files_confirm(event):
                neural_network_files = self.neural_network_files_input.value
                py_found = False
                txt_found = False
                if len(neural_network_files)==2:
                    for f in neural_network_files:
                        if f.endswith(".py"):
                            self.settings['neural_network_python_script_path'] = f
                            py_found = True
                        elif f.endswith(".txt"):
                            self.settings['neural_network_requirements_txt_path'] = f
                            txt_found = True
                if py_found and txt_found:
                    print(py_found, txt_found)
                    #self.neural_network_files_input.disabled = True
                    self.buttons_dict['neural_network_files_confirm_button'].disabled = True

            if include_neural_network:
                self.neural_network_files_input = pn.widgets.FileSelector('~', width=400, height=400, margin=10)
                self.formatting_requirements = pn.widgets.TextAreaInput(name='Requirements for formatting the Python script', 
                                                                        width=1000, min_height=1000, margin=10)
                curr_dir = os.path.abspath(os.path.dirname( __file__ ))
                fmt_reqs = open(os.path.join(curr_dir, "neural_network_script_formatting_requirements.txt")).read()
                self.formatting_requirements.value = fmt_reqs
                self.formatting_requirements.disabled = True
                self.buttons_dict['neural_network_files_confirm_button'] = pn.widgets.Button(name='Confirm configuration', button_type='primary', 
                                                                                             margin=20, width=100)
                self.buttons_dict['neural_network_files_confirm_button'].on_click(neural_network_files_confirm) 
                self.settings_GUI.main[0][4] = pn.Column(pn.WidgetBox("### Please select a Python script (.py) that trains and tests a neural network. To make it compatible with \
                                                                           the model comparison software, it must be formatted according to the guidelines shown on the right. \
                                                                           Please also provide a requirements file (.txt) for the installation of the packages required for the script",
                                                                      pn.Row(pn.Column(self.neural_network_files_input, self.buttons_dict['neural_network_files_confirm_button']), 
                                                                             self.formatting_requirements), 
                                                                      width=1600))
            else:
                self.settings['neural_network_python_script_path'] = ""
                self.settings['neural_network_requirements_txt_path'] = ""
            
        self.buttons_dict['include_nn_confirm_button'] = pn.widgets.Button(name='Confirm configuration', button_type='primary', margin=20,
                                                       width=100, align=('center'))
        self.buttons_dict['include_nn_confirm_button'].on_click(include_nn_confirm) 

    def create_start_analysis_confirm_button(self):
        def start_analysis_confirm(event):
            all_widgets_inputs_confirmed = True
            for button_name, button in self.buttons_dict.items():
                if not button.disabled:
                    all_widgets_inputs_confirmed = False
                    break
            if all_widgets_inputs_confirmed:
                self.start_analysis_confirm_button.disabled = True
                self.event_lock.set()

        self.start_analysis_confirm_button = pn.widgets.Button(name='Start Analysis', button_type='primary', margin=20,
                                                       width=100, align=('center'))
        self.start_analysis_confirm_button.on_click(start_analysis_confirm)
        
    def run_interactive_gui(self):
        # get input from port
        self.input_data = self.inputs['input_data']

        self.labels_input = pn.widgets.MultiSelect(name='Select label(s)', options=self.input_data.columns.tolist(), width=300, margin=10)
        self.create_labels_confirm_button()
        self.numbers_for_rfe_input = pn.widgets.MultiSelect(name='Select number(s) for RFE', options=[], width=300, margin=10, disabled=True)
        self.create_numbers_for_rfe_confirm_button()
        
        self.analysis_name_input = pn.widgets.TextInput(name="Analysis Name", width=200, margin=10)
        self.results_name_input = pn.widgets.TextInput(name="Results Name", width=200, margin=10)
        self.storage_path_input = pn.widgets.FileSelector('~', width=400, margin=10)
        self.create_save_dir_confirm_button()
        
        self.generate_learning_curve_cb = pn.widgets.Checkbox(name='Generate learning curves', value=True, margin=10)
        self.create_generate_lc_confirm_button()
        
        self.include_neural_network_cb = pn.widgets.Checkbox(name='Include neural network in the model comparison', margin=10)
        self.create_include_nn_confirm_button()
        
        self.create_start_analysis_confirm_button()

        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Configuration of the software for comparing model performance",

            main=[pn.Column(
                pn.Column(pn.WidgetBox('### Select the label(s) and the number(s) of the most important features that you want \
                                            to select using recursive feature elimination (RFE)',
                                       pn.Row(self.labels_input, self.buttons_dict['labels_confirm_button']), 
                                       pn.Row(self.numbers_for_rfe_input, self.buttons_dict['numbers_for_rfe_confirm_button']),
                                       width=700)),
                pn.Column(pn.WidgetBox('### The results (data frames and diagrams) and other data are saved under "Storage path/analysis name"',
                                       pn.Row(self.analysis_name_input, self.results_name_input),
                                       pn.Column("Storage path",
                                                 self.storage_path_input),
                                       self.buttons_dict['save_dir_confirm_button'],
                                       width=700)),
                pn.Column(pn.WidgetBox('### The learning curves show the training and validation error of each model for different fractions of the training set',
                                       pn.Row(self.generate_learning_curve_cb, self.buttons_dict['generate_lc_confirm_button']),
                                       width=700)),
                pn.Column(pn.WidgetBox('### Compare the performance of your own Python script for training neural networks',
                                       pn.Row(self.include_neural_network_cb, self.buttons_dict['include_nn_confirm_button']),
                                       width=700)),
                pn.Spacer(width=50),
                self.start_analysis_confirm_button)
            ],
        )

        self._show_layout()
        return self.settings