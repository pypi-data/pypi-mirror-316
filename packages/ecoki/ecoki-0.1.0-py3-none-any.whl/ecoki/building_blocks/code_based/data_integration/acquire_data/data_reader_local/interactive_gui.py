# System imports
import panel as pn
import threading
from pyDataverse.api import NativeApi
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI

pn.config.notifications = True


class InteractiveGUI(AbstractInteractiveGUI):
    """user interface"""

    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.widgets_dict = {}

        self.widgets_box_upload_file_config = pn.WidgetBox("# Upload local csv file")

        self.layout = pn.Column(self.widgets_box_upload_file_config,
            pn.Spacer(height=70),
            pn.Row(),
            pn.Spacer(height=50),
            pn.Column())

        self.create_widgets()
        self.create_buttons()

    def create_widgets(self):
        # file_selector = pn.widgets.FileInput(accept='.csv,.json', width=500)
        file_selector = pn.widgets.FileSelector('~')
        self.widgets_dict["local_dataset"] = file_selector
        index_selector = pn.widgets.Select(name='Select Index Column')
        column_separator = pn.widgets.Select(name='Column Separator', width=250)
        column_separator.options = [""] + [";", ","]
        self.widgets_dict["index_selector"] = index_selector
        self.widgets_dict["columns_separator"] = column_separator

        self.widgets_box_upload_file_config.extend([self.widgets_dict["local_dataset"]])

        inverted = pn.widgets.Checkbox(name='Invert Dataset?')
        self.widgets_dict["invert_data"] = inverted

        self.layout[2].extend([self.widgets_dict["index_selector"]])
        self.layout[2].extend([self.widgets_dict["invert_data"]])
        self.layout[0].extend([self.widgets_dict["columns_separator"]])

    def create_buttons(self):
        def select_datafile(event):
            self.settings["data_file_path"] = self.widgets_dict["local_dataset"].value[0]
            self.settings["columns_separator"] = self.widgets_dict["columns_separator"].value

            self.building_block.upload_local_dataset(self.settings["data_file_path"], self.settings["columns_separator"])
            df_columns = [""] + self.building_block.dataset.columns.tolist()
            self.widgets_dict["index_selector"].options = df_columns
            self.widgets_dict["local_csv_button"].disabled = True

        def confirm_configuration(event):
            self.settings["index_name"] = self.widgets_dict["index_selector"].value
            self.settings["invert_data"] = self.widgets_dict["invert_data"].value
            self.widgets_dict["confirm_configuration"].disabled = True
            self.event_lock.set()

        datafile_button = pn.widgets.Button(name='Select csv file', button_type='primary', align='center', width=300)
        datafile_button.on_click(select_datafile)
        self.widgets_dict["local_csv_button"] = datafile_button
        self.widgets_box_upload_file_config.extend([self.widgets_dict["local_csv_button"]])

        confirm_button = pn.widgets.Button(name='Confirm Configuration', button_type='primary', align='center', width=300)
        confirm_button.on_click(confirm_configuration)
        self.widgets_dict["confirm_configuration"] = confirm_button
        self.layout[4].extend([self.widgets_dict["confirm_configuration"]])

    def disable_all_buttons(self):
        if not self.widgets_dict["local_csv_button"].disabled:
            self.widgets_dict["local_csv_button"].disabled = True

    def run_interactive_gui(self):
        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="ecoKI Local Data Reader",

            main=[self.layout
            ],
        )
        self._show_layout()

        return self.settings