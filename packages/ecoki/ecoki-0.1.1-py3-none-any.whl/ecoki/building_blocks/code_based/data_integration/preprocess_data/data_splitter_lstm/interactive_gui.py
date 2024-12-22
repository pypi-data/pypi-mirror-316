# System imports
import pandas as pd
import panel as pn
import threading
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
import io

pn.config.notifications = True
#pn.extension(sizing_mode="stretch_width")


class InteractiveGUI(AbstractInteractiveGUI):
    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.test_dataset_size = None
        self.test_dataset_size_confirm_button = None

    def create_test_dataset_size_confirm_button(self):
        def confirm(event):
            test_dt_size = self.test_dataset_size.value
            if test_dt_size:
                self.settings['test_dataset_size'] = test_dt_size
                self.test_dataset_size_confirm_button.disabled = True
                self.event_lock.set()

        self.test_dataset_size_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                       width=100,
                                                       align='end')
        self.test_dataset_size_confirm_button.on_click(confirm)

    def run_interactive_gui(self):
        self.test_dataset_size = pn.widgets.Select(options=[0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4], width=100)
        self.create_test_dataset_size_confirm_button()

        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Konfiguration der Größe des Testdatensatzes für den Dataset-Splitter",

            main=[pn.Column(
                pn.Column(pn.WidgetBox('### Geben Sie den Dezimalbruch des gesamten Datensatzes an, der für die Testen verwendet werden soll', 
                                        self.test_dataset_size, width=500),
                          pn.Column(self.test_dataset_size_confirm_button, margin=(25, 0, 0, 0))),)
            ],
        )
        self._show_layout()
        return self.settings