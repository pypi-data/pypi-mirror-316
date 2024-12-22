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

        self.sample_time_resolution_input = None
        self.time_resolution_confirm_button = None

    def create_time_resolution_confirm_button(self):
        def confirm(event):
            datetime_sampling_resolution = self.sample_time_resolution_input.value
            if datetime_sampling_resolution:
                self.settings['datetime_sampling_resolution'] = datetime_sampling_resolution
                self.time_resolution_confirm_button.disabled = True
                self.event_lock.set()

        self.time_resolution_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                       width=100,
                                                       align='end')
        self.time_resolution_confirm_button.on_click(confirm)

    def run_interactive_gui(self):
        self.sample_time_resolution_input = pn.widgets.Select(options=["D", "H", "10T", "20T", "30T"], margin=10, width=100)
        self.create_time_resolution_confirm_button()

        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Konfiguration der zeitlichen Auflösung der Datensatz probenahme (Tag, Stunde oder Minute)",

            main=[pn.Column(
                pn.Column(pn.WidgetBox('### Wählen Sie die Auflösung der Stichprobenzeit in Tagen, Stunden oder Minuten. \
                                            Die Zeilen des Datensatzes werden dann entsprechend gruppiert. T steht für Minute', 
                                        self.sample_time_resolution_input, width=500),
                          pn.Column(self.time_resolution_confirm_button, margin=(25, 0, 0, 0))), 
                pn.Spacer(width=50),
                pn.Spacer(width=50),)
            ],
        )
        self._show_layout()
        return self.settings