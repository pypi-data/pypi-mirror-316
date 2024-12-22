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
        self.button_dict = {}

        self.layout = pn.Column(
            pn.Column(pn.WidgetBox("## Datenbank Server Konfiguration")),
            pn.Spacer(width=100),
            pn.Column(),
            pn.Spacer(width=100),
            pn.Column(),
            pn.Spacer(width=100),
            pn.Column()
        )

        self.create_widgets()
        self.create_buttons()

    def create_widgets(self):
        database_host_selector = pn.widgets.Select(name='Default MongoDB Server Url:', options=["mongodb://localhost:27017/", "mongodb://141.76.56.139:27017/"], width=500)
        database_host_url_input = pn.widgets.TextInput(name='MongoDB Server Url:', placeholder='Geben Sie die URL des Mongodb-Servers ein ...', width=500)

        database_host_url = pn.Column(database_host_selector, database_host_url_input)

        database_selection = pn.widgets.Select(name='Datenbank auswählen', options=[], width=500)

        collection_selection = pn.widgets.Select(name='Datenbank Sammelung auswählen', options=[], width=500)

        text_number_of_documents = pn.widgets.TextInput(name='Anzahl der MongoDB-Dokumente:', value="2000",
                                                        placeholder='Anzahl der Dokumente...')

        static_text_collection = pn.widgets.StaticText(name='Ausgewählte Sammlung: ', width=500)
        static_text_num_docs = pn.widgets.StaticText(name='Anzahl der Dokumente: ', width=500)

        reindex_column_name = pn.widgets.TextInput(name='Index: ', value="timestamp",
                                                   placeholder='Enter index column name...', width=500)

        self.widgets_dict["database_url"] = database_host_url
        self.widgets_dict["database_selection"] = database_selection
        self.widgets_dict["collection_selection"] = collection_selection
        self.widgets_dict["number_documents"] = text_number_of_documents
        self.widgets_dict["text_collection"] = static_text_collection
        self.widgets_dict["text_num_docs"] = static_text_num_docs
        self.widgets_dict["reindex_column_name"] = reindex_column_name

        self.layout[0][0].append(self.widgets_dict["database_url"])

    def create_buttons(self):
        def connect_to_database_server(event):
            if self.layout[2]:
                self.layout[2] = pn.Column()

            database_url_widgets = self.widgets_dict["database_url"]
            if database_url_widgets[1].value:
                database_url = database_url_widgets[1].value
            else:
                database_url = database_url_widgets[0].value

            self.building_block.mongodb_client.connect_to_mongodb_sever(database_url)
            self.settings["database_url"] = database_url
            self.widgets_dict["database_selection"].options = self.building_block.mongodb_client.get_database_list()

            database_widget_box = pn.WidgetBox("## Datenbank Konfiguration",
                                               self.widgets_dict["database_selection"],
                                               self.button_dict["database_selection"])
            self.layout[2].insert(0, database_widget_box)

        def select_database(event):
            if self.layout[4]:
                self.layout[4] = pn.Column()

            database_name = self.widgets_dict["database_selection"].value
            self.building_block.mongodb_client.get_database(database_name)
            self.settings["database_name"] = database_name
            collection_list = self.building_block.mongodb_client.get_collection_list()
            self.widgets_dict["collection_selection"].options = collection_list

            collection_widget_box = pn.WidgetBox("## Datenbank Sammlung Konfiguration",
                                                 self.widgets_dict["collection_selection"],
                                                 self.widgets_dict["number_documents"],
                                                 self.button_dict["collection_selection"])
            self.layout[4].insert(0, collection_widget_box)

        def select_collection(event):
            if self.layout[6]:
                self.layout[6] = pn.Column()

            collection = self.widgets_dict["collection_selection"].value
            number_of_documents = self.widgets_dict["number_documents"].value
            self.widgets_dict["text_collection"].value = collection

            if number_of_documents:
                self.widgets_dict["text_num_docs"].value = number_of_documents

            confirmation_widget_box = pn.WidgetBox("## Übersicht über die Konfiguration",
                                                   self.widgets_dict["text_collection"],
                                                   self.widgets_dict["text_num_docs"],
                                                   self.widgets_dict["reindex_column_name"],
                                                   self.button_dict["confirm"])
            self.layout[6].insert(0, confirmation_widget_box)

        def confirm_configuration(event):
            self.settings["collection"] = self.widgets_dict["collection_selection"].value
            if self.widgets_dict["number_documents"].value:
                self.settings["number_documents"] = int(self.widgets_dict["number_documents"].value)
            else:
                self.settings["number_documents"] = None

            index_column = self.widgets_dict["reindex_column_name"].value
            if index_column:
                self.settings["index_name"] = index_column
            else:
                self.settings["index_name"] = None

            self.button_dict["confirm"].disabled = True
            self.event_lock.set()

        button_url = pn.widgets.Button(name='Verbindung zum Datanbankserver herstellen', button_type='primary')
        button_url.on_click(connect_to_database_server)

        button_database = pn.widgets.Button(name='Auswahl der Datenbank bestätigen', button_type='primary')
        button_database.on_click(select_database)

        button_collection = pn.widgets.Button(name='Auswahl der Datenbank Sammlung bestätigen', button_type='primary')
        button_collection.on_click(select_collection)

        button_confirm = pn.widgets.Button(name='Konfiguration bestätigen', button_type='primary')
        button_confirm.on_click(confirm_configuration)

        self.button_dict["database_url"] = button_url
        self.button_dict["database_selection"] = button_database
        self.button_dict["collection_selection"] = button_collection
        self.button_dict["confirm"] = button_confirm

        self.layout[0][0].append(self.button_dict["database_url"])

    def disable_all_buttons(self):
        for button_name, button in self.button_dict.items():
            if not button.disabled:
                button.disabled = True

    def run_interactive_gui(self):
        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="MongoDB Konfiguration",

            main=[self.layout],
        )

        self._show_layout()
        return self.settings
