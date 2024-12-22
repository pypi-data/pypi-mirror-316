# System imports
import panel as pn
import threading
import importlib

from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
from ecoki.building_blocks.code_based.data_integration.acquire_data.ecoki_data_reader.data_reader_register import \
    DataReaderGUIRegister
from ecoki.common.module_object_creator import create_object_by_module

pn.config.notifications = True


class InteractiveGUI(AbstractInteractiveGUI):
    """user interface"""

    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.data_reader_gui_set = {}
        self.data_reader_tab_set = None
        self.confirm_buttons = {}

        self.register_data_reader_gui(endpoint, port)

        self.create_confirm_buttons()
        self.create_data_reader_tabs()

    def register_data_reader_gui(self, endpoint, port):
        for data_reader_name, data_reader in self.building_block.data_reader_dict.items():
            self.create_data_reader_gui(data_reader_name, endpoint, port, data_reader)

    def create_data_reader_gui(self, data_reader_name, endpoint, port, building_block):
        self.data_reader_gui_set[data_reader_name] = create_object_by_module(
            eval(f"DataReaderGUIRegister.{data_reader_name}.value"),
            "InteractiveGUI",
            endpoint=endpoint,
            port=port,
            building_block=building_block)

    def disable_button(self):
        for confirm_button in self.confirm_buttons.values():
            confirm_button.disabled = True

    def disable_all_buttons(self):
        for data_reader_gui in self.data_reader_gui_set.values():
            data_reader_gui.disable_all_buttons()

    def create_confirm_buttons(self):

        def data_reader_gui_click(button_name):
            self.settings = self.data_reader_gui_set[button_name].settings
            self.disable_button()
            self.disable_all_buttons()
            self.settings["data_reader"] = button_name
            self.event_lock.set()

        for data_reader_name, data_reader_gui in self.data_reader_gui_set.items():
            self.confirm_buttons[data_reader_name] = pn.widgets.Button(name=data_reader_name,
                                                                       button_type='primary', align='center',
                                                                       width=300)
            self.confirm_buttons[data_reader_name].on_click(
                lambda event, button_name=data_reader_name: data_reader_gui_click(button_name))

        for data_reader_gui_name, data_reader_gui in self.data_reader_gui_set.items():
            data_reader_gui.layout.append(pn.Column(self.confirm_buttons[data_reader_gui_name]))

    def create_data_reader_tabs(self):
        self.data_reader_tab_set = pn.Tabs()
        for data_reader_gui_name, data_reader_gui in self.data_reader_gui_set.items():
            self.data_reader_tab_set.append((data_reader_gui_name, data_reader_gui.layout))

    def run_interactive_gui(self):
        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="EcoKI Data Reader",

            main=self.data_reader_tab_set
        )

        self._show_layout()

        return self.settings
