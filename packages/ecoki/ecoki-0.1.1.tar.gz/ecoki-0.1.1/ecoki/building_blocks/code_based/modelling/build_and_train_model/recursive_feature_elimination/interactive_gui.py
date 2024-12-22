# System imports
import pandas as pd
import panel as pn
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
import json
import threading


class InteractiveGUI(AbstractInteractiveGUI):
    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.selected_columns = []  # gui widgets specific attribute
        self.components_checkbox = {}  # gui widgets specific attribute
        self.checkbox_list = []  # gui widgets specific attribute
        self.button = None  # gui widgets specific attribute

        self.inputs_name = ["input_data"]  # gui input name list, empty, if no input is required

        self.option_buttons = []

        self.components_checkbox = {}
        self.checkbox_list = []

        self.file_input = None

        self.select_widgets = []
        self.manual_config_tabs = pn.Tabs()
        self.file_select = pn.widgets.FileSelector('~')

        self.buttons = {}
        self.selected_columns = []
        self.selected_columns_label = []
        self.selectedEstimator = []
        self.event_lock_label = threading.Event()
        self.event_lock_rfe = threading.Event()
        self.min_features_to_select = 1

    def select_rfe_method_checkbox(self):
        rfe_method_options = ['classification', 'regression']

        rfe_method_select = pn.widgets.Select(
            name='RFE Method',
            options=rfe_method_options,
            width=200
        )

        columns_classification = ['SVC', 'DecisionTreeClassifier', 'RandomForestClassifier',
                                  'GradientBoostingClassifier','XGBClassifier']
        columns_regression = ['SVR', 'DecisionTreeRegressor', 'RandomForestRegressor', 'GradientBoostingRegressor','XGBRegressor']

        features = pn.widgets.MultiSelect(
            name='Select columns',
            value=list(columns_classification),
            options=list(columns_classification),
            width=500,
            height=400
        )
        panel_columns = pn.Column(
            pn.pane.Markdown('## RFE method Selection', align='center'),
            features,
            background='WhiteSmoke'
        )

        # min_features_input = pn.widgets.IntSlider(
        #     name='Hyperparameter for RFE: Min Features to Select',
        #     start=1,
        #     end=10,
        #     value=1,
        #     step=1,
        #     width=200
        # )

        def select_features(event):
            self.selectedEstimator.extend(features.value)
            # self.min_features_to_select = min_features_input.value
            self.event_lock_rfe.set()

        def update_columns(event):
            if rfe_method_select.value == 'classification':
                features.options = list(columns_classification)
            elif rfe_method_select.value == 'regression':
                features.options = list(columns_regression)


        button = pn.widgets.Button(name='Confirm Selection', button_type='primary')
        button.on_click(select_features)

        rfe_method_select.param.watch(update_columns, 'value')

        return pn.Column(
            '# Select RFE method',
            ' ',
            pn.Column(rfe_method_select),
            pn.Column(panel_columns),
            # pn.Column(min_features_input),
            pn.Column(button),
            sizing_mode='stretch_both'
        )

    def select_columns_panel_checkbox(self, doc_df):
        columns = [col for col in doc_df.columns]
        #columns.append("timestamp")
        #columns = doc_df[value_columns].copy()

        features = pn.widgets.MultiSelect(name='Select columns', value=list(columns),
                                                     options=list(columns), width = 500, height = 400)
        panel_columns = pn.Column(pn.pane.Markdown('## Training features Selection', align='center'),
                                  features,
                                  background='WhiteSmoke')

        def select_features(event):
            self.selected_columns.extend(features.value)
            self.event_lock.set()
            #print(features.value)


        button = pn.widgets.Button(name='Confirm Selection', button_type='primary')

        button.on_click(select_features)

        return pn.Column('# Select Feature Columns', ' ', pn.Column(panel_columns),
                  pn.Column(button),  sizing_mode='stretch_both')

    def select_label_features_panel_checkbox(self, doc_df):
        #columns = doc_df.columns
        columns = [col for col in doc_df.columns]

        labels = pn.widgets.MultiSelect(name='Select columns', value=list(columns),
                                                     options=list(columns), width = 500, height = 400)
        panel_columns = pn.Column(pn.pane.Markdown('## Training labels', align='center'),
                                  labels,
                                  background='WhiteSmoke')

        def select_label_features(event):
            self.selected_columns_label.extend(labels.value)
            self.event_lock_label.set()
            #print(labels.value)


        button = pn.widgets.Button(name='Confirm Selection', button_type='primary')

        button.on_click(select_label_features)

        return pn.Column('# Select Label Columns', ' ', pn.Column(panel_columns),
                  pn.Column(button),  sizing_mode='stretch_both')


    def run_interactive_gui(self):
        input_df = self.inputs["input_data"]
        print("\n")
        print("the head of input_df is \n", input_df.head())
        print("\n")
        doc_df = input_df.copy()
        select_features_gui = self.select_columns_panel_checkbox(doc_df)
        select_label_features_gui = self.select_label_features_panel_checkbox(doc_df)
        select_rfe_method_gui = self.select_rfe_method_checkbox()
        panel_plots = pn.Tabs()
        panel_plots.append(("Select Features", pn.WidgetBox("### Select Features", select_features_gui)),

                           )
        panel_plots.append(
            ("Select Label Features", pn.WidgetBox("### Select Label Features", select_label_features_gui)))
        panel_plots.append(("Select RFE method", pn.WidgetBox("### Select RFE method", select_rfe_method_gui)))
        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Data Conversion Dashboard",
            main=[panel_plots],
        )


        self._show_layout()
        self.event_lock_label.wait()
        self.event_lock_rfe.wait()

        self.settings["selected_columns"] = self.selected_columns
        self.settings["selected_columns_label"] = self.selected_columns_label
        self.settings["selectEstimator"] = self.selectedEstimator
        # self.settings["min_features_to_select"] = self.min_features_to_select

        print("\n the settings are \n", self.settings)
        return self.settings
