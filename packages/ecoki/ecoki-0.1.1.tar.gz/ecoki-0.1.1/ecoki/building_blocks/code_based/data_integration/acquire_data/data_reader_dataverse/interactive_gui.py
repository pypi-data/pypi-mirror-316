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
        self.data_files_dict = {}

        self.widgets_box_connection = pn.WidgetBox("# Dataverse Connection")
        self.widgets_box_selection = pn.WidgetBox("# Datafile Selection")
        self.widgets_box_index = pn.WidgetBox("# Index/Reindex Column", width=500)

        self.layout = pn.Column(self.widgets_box_connection,
                                pn.Spacer(width=70),
                                self.widgets_box_selection,
                                pn.Spacer(width=70),
                                self.widgets_box_index)
        self.create_widgets()
        self.create_buttons()

    def create_widgets(self):
        dataverse_host_widget = pn.widgets.TextInput(name='Dataverse Host:', value="https://demo.dataverse.org/",
                                                     placeholder='Enter dataverse host...', width=500)

        dataverse_doi_widget = pn.widgets.TextInput(name='Dataset DOI:',
                                                    value="doi:10.70122/FK2/CDISCB",
                                                    placeholder='Enter dataset DOI...', width=500)

        self.widgets_dict["dataverse_connection"] = {"host": dataverse_host_widget, "doi": dataverse_doi_widget}

        select_datafile = pn.widgets.Select(name='Select Datafile:', width=500)

        self.widgets_dict["datafile"] = {"datafile": select_datafile}

        index_selector = pn.widgets.Select(name='Select Index Column')
        self.widgets_dict["index_selector"] = index_selector

    def create_buttons(self):
        def select_datafile(event):
            datafile_name = self.widgets_dict["datafile"]["datafile"].value
            datafile_id = self.data_files_dict[datafile_name]
            self.settings["id"] = datafile_id

            self.building_block.download_from_dataverse(self.settings["base_url"], self.settings["token"],
                                                        self.settings["id"])
            df_columns = [""]+ self.building_block.data.columns.tolist()
            self.widgets_dict["index_selector"].options = df_columns
            self.widgets_dict["datafile"]["button"].disabled = True
            # self.event_lock.set()

        def dataverse_host_connection(event):
            dataverse_host = self.widgets_dict["dataverse_connection"]["host"].value
            API_TOKEN = "a2860ad5-e11a-4f48-a740-72e52fd943ce"
            api = NativeApi(dataverse_host, API_TOKEN)

            dataverse_doi = self.widgets_dict["dataverse_connection"]["doi"].value

            pn.state.notifications.position = 'center-center'
            pn.state.notifications.success('Connected to Dataverse Host successfully.')

            self.settings["base_url"] = dataverse_host
            self.settings["token"] = API_TOKEN
            dataset = api.get_dataset(dataverse_doi)
            data_files_list = dataset.json()['data']['latestVersion']['files']

            for datafile in data_files_list:
                filename = datafile["dataFile"]["filename"]
                file_id = datafile["dataFile"]["id"]
                self.data_files_dict[filename] = file_id

            self.widgets_dict["datafile"]["datafile"].options = list(self.data_files_dict.keys())

        def confirm_configuration(event):
            self.settings["index_name"] = self.widgets_dict["index_selector"].value

            self.widgets_dict["confirm_configuration"].disabled = True
            self.event_lock.set()

        dataverse_host_button = pn.widgets.Button(name='Connect to Dataverse Host', button_type='primary',
                                                  align='center', width=300)
        dataverse_host_button.on_click(dataverse_host_connection)
        self.widgets_dict["dataverse_connection"]["button"] = dataverse_host_button
        self.widgets_box_connection.extend(list(self.widgets_dict["dataverse_connection"].values()))

        datafile_button = pn.widgets.Button(name='Select Datafile', button_type='primary', align='center', width=300)
        datafile_button.on_click(select_datafile)
        self.widgets_dict["datafile"]["button"] = datafile_button
        self.widgets_box_selection.extend(list(self.widgets_dict["datafile"].values()))

        confirm_button = pn.widgets.Button(name='Confirm Configuration', button_type='primary', align='center',
                                           width=300)
        confirm_button.on_click(confirm_configuration)
        self.widgets_dict["confirm_configuration"] = confirm_button
        self.widgets_box_index.extend([self.widgets_dict["index_selector"], self.widgets_dict["confirm_configuration"]])

    def disable_all_buttons(self):
        if not self.widgets_dict["datafile"]["button"].disabled:
            self.widgets_dict["datafile"]["button"].disabled = True

        if not self.widgets_dict["dataverse_connection"]["button"].disabled:
            self.widgets_dict["dataverse_connection"]["button"].disabled = True

    def run_interactive_gui(self):
        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="ecoKI Dataverse Configuration",

            main=[self.layout
            ],
        )
        self._show_layout()

        return self.settings
