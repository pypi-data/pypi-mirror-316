# System imports
import pandas as pd
import panel as pn
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
import threading


class InteractiveGUI(AbstractInteractiveGUI):
    """
    A class to create and manage an interactive GUI for selecting features and labels from a dataset.

    Parameters
    ----------
    endpoint : str
        The endpoint for the GUI.
    port : int
        The port for the GUI.
    building_block : str
        The building block for the GUI.

    Attributes
    ----------
    selected_columns : list
        A list to store the selected feature columns.
    components_checkbox : dict
        A dictionary to store the components of the checkbox.
    checkbox_list : list
        A list to store the checkboxes.
    button : pn.widgets.Button or None
        A button widget for the GUI.
    inputs_name : list
        A list containing the names of the inputs.
    option_buttons : list
        A list to store option buttons.
    file_input : NoneType
        A variable to store file input, currently not implemented.
    select_widgets : list
        A list to store selected widgets.
    manual_config_tabs : pn.Tabs
        A Tabs widget for manual configuration.
    file_select : pn.widgets.FileSelector
        A FileSelector widget for file selection.
    buttons : dict
        A dictionary to store buttons.
    selected_columns_label : list
        A list to store the selected label columns.
    event_lock_label : threading.Event
        A threading event lock for label selection.

    Methods
    -------
    select_columns_panel_checkbox(doc_df)
        Creates a panel with checkboxes for selecting feature columns.
    select_label_features_panel_checkbox(doc_df)
        Creates a panel with checkboxes for selecting label columns.
    run_interactive_gui()
        Runs the interactive GUI and returns the settings for selected columns and label columns.
    """
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
        self.event_lock_label = threading.Event()


    def select_columns_panel_checkbox(self, doc_df):
        """
        Creates a panel with checkboxes for selecting feature columns.

        Parameters
        ----------
        doc_df : pandas.DataFrame
            The input data.

        Returns
        -------
        panel_columns : panel.Column
            The panel with the checkboxes for selecting feature columns.
        """
        columns = [col for col in doc_df.columns]

        features = pn.widgets.MultiSelect(name='Select columns', value=list(columns),
                                                     options=list(columns), width = 500, height = 400)
        panel_columns = pn.Column(pn.pane.Markdown('## Training features Selection', align='center'),
                                  features,
                                  background='WhiteSmoke')

        def select_features(event):
            self.selected_columns.extend(features.value)
            self.event_lock.set()

        button = pn.widgets.Button(name='Confirm Selection and Create Tabular Data', button_type='primary')

        button.on_click(select_features)

        return pn.Column('# Select Feature Columns', ' ', pn.Column(panel_columns),
                  pn.Column(button),  sizing_mode='stretch_both')

    def select_label_features_panel_checkbox(self, doc_df):
        """
        Creates a panel with checkboxes for selecting label columns.

        Parameters
        ----------
        doc_df : pandas.DataFrame
            The input data.

        Returns
        -------
        panel_columns : panel.Column
            The panel with the checkboxes for selecting label columns.
        """
        columns = [col for col in doc_df.columns]

        labels = pn.widgets.MultiSelect(name='Select columns', value=list(columns),
                                                     options=list(columns), width = 500, height = 400)
        panel_columns = pn.Column(pn.pane.Markdown('## Training labels', align='center'),
                                  labels,
                                  background='WhiteSmoke')

        def select_label_features(event):
            self.selected_columns_label.extend(labels.value)
            self.event_lock_label.set()

        button = pn.widgets.Button(name='Confirm Selection and Create Tabular Data', button_type='primary')

        button.on_click(select_label_features)

        return pn.Column('# Select Label Columns', ' ', pn.Column(panel_columns),
                  pn.Column(button),  sizing_mode='stretch_both')


    def run_interactive_gui(self):
        """
        Runs the interactive GUI.

        Returns
        -------
        settings : dict
            The settings for the selected columns and label columns.
        """
        input_df = self.inputs["input_data"]
        print("\n")
        print("the head of input_df is \n", input_df.head())
        print("\n")
        doc_df = input_df.copy()
        select_features_gui = self.select_columns_panel_checkbox(doc_df)
        select_label_features_gui = self.select_label_features_panel_checkbox(doc_df)
        panel_plots = pn.Tabs()
        panel_plots.append(("Select Features", pn.WidgetBox("### Select Features", select_features_gui)),

                           )
        panel_plots.append(
            ("Select Label Features", pn.WidgetBox("### Select Label Features", select_label_features_gui)))
        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Data Conversion Dashboard",
            main=[panel_plots],
        )


        self._show_layout()
        self.event_lock_label.wait()

        self.settings = self.building_block.settings
        self.settings["selected_columns"] = self.selected_columns
        self.settings["selected_columns_label"] = self.selected_columns_label
        return self.settings
