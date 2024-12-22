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

        self.num_input_steps_input = None
        self.num_output_steps_input = None
        self.num_steps_confirm_button = None

    def create_num_steps_confirm_button(self):
        def confirm(event):
            ip_steps_num = self.num_input_steps_input.value
            op_steps_num = self.num_output_steps_input.value
            print(ip_steps_num, op_steps_num)
            if ip_steps_num and op_steps_num:
                self.settings['num_steps_in'] = ip_steps_num
                self.settings['num_steps_out'] = op_steps_num
                self.num_steps_confirm_button.disabled = True
                self.event_lock.set()

        self.num_steps_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                       width=100,
                                                       align='end')
        self.num_steps_confirm_button.on_click(confirm)

    def run_interactive_gui(self):
        self.num_input_steps_input = pn.widgets.Select(options=list(range(10, 51)), width=100)
        self.num_output_steps_input = pn.widgets.Select(options=list(range(10, 51)), width=200, margin=10)
        self.create_num_steps_confirm_button()

        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Konfiguration der Zeitschritte für den Datensequenzer",

            main=[pn.Column(
                pn.Column(pn.WidgetBox('## Wählen Sie die Anzahl der Eingabe- und Ausgabeschritte für die Erzeugung der Datenfolgen.', 
                                        "### Eingabeschritte",
                                        self.num_input_steps_input,
                                        "### Ausgabeschritte",
                                        self.num_output_steps_input, width=500),
                          pn.Column(self.num_steps_confirm_button, margin=(25, 0, 0, 0))),)
            ],
        )
        self._show_layout()
        return self.settings