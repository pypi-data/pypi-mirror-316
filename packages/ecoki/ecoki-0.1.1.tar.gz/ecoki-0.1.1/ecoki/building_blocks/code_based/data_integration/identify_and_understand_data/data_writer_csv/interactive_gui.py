# System imports
import panel as pn
import json
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI


class InteractiveGUI(AbstractInteractiveGUI):
    """user interface"""

    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)
        self.database_widgets = {}
        self.collection_widgets = {}

    def enter_database_config(self):
        select_database_url = pn.widgets.Select(name='Select database url:', options=["mongodb://141.76.56.139:27017/",
                                                                                      "mongodb://localhost:27017/"])
        text_database_name = pn.widgets.TextInput(name='Database Name:', value="Appliances_Energy_Prediction",
                                                  placeholder='Enter database name...')
        self.database_widgets["url"] = select_database_url
        self.database_widgets["name"] = text_database_name
        database_layout = pn.Row(select_database_url, text_database_name, background='LightGray')
        return database_layout

    def enter_collection_config(self):
        text_collection_name = pn.widgets.TextInput(name='Collection Name:', value='energy_data_complete_nan',
                                                    placeholder='Enter collection name...')

        text_csv_file_path = pn.widgets.TextInput(name='csv file path:', value='ecoki/datasets/appliances_nans.csv')

        text_config_file_path = pn.widgets.TextInput(name='mapping file path:',
                                                     value="ecoki/building_blocks/code_based/data_integration/identify_and_understand_data/data_writer_csv/data_mapping_config/",
                                                     placeholder='Enter mapping file path...')
        self.collection_widgets["name"] = text_collection_name
        self.collection_widgets["csv_file_path"] = text_csv_file_path
        self.collection_widgets["mapping_file_path"] = text_config_file_path

        col_layout = pn.Column(text_collection_name, text_csv_file_path, text_config_file_path, background='LightGray')

        return col_layout

    def run_interactive_gui(self, **kwargs):
        def data_writer_config(event):
            database_url = self.database_widgets["url"].value
            database_name = self.database_widgets["name"].value

            database_config = {"url": database_url, "database_name": database_name}
            collection_name = self.collection_widgets["name"].value

            collections_list = []

            csv_file_path = self.collection_widgets["csv_file_path"].value
            mapping_file_path = self.collection_widgets["mapping_file_path"].value

            collection_dict = {"file": csv_file_path, "mapping": mapping_file_path}

            collections_list.append({collection_name: [collection_dict]})
            database_config["collections"] = collections_list

            # DBMS_service_config_json = json.dumps({"write_data": {"database": database_config}})
            DBMS_service_config_json = {"write_data": {"database": database_config}}
            self.settings = DBMS_service_config_json

            self.event_lock.set()

        # create button widget
        button = pn.widgets.Button(name='confirm and save configuration', button_type='primary')

        # button with on click
        button.on_click(data_writer_config)

        database_layout = self.enter_database_config()
        col_layout = self.enter_collection_config()

        panel_data_writer = pn.Column('# Database Configuration', database_layout, '# Collection Configuration',
                                      col_layout, "# save Configuration", button)

        self.settings_GUI = panel_data_writer

        self._show_layout()

        return self.settings
