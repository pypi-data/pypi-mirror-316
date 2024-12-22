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

        self.row_hist_input = None
        self.row_hist_confirm_button = None

    def create_row_hist_confirm_button(self):
        def confirm(event):
            row_history = self.row_hist_input.value
            if row_history:
                self.settings['row_history'] = row_history
                self.row_hist_confirm_button.disabled = True
                self.event_lock.set()

        self.row_hist_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                       width=100,
                                                       align='end')
        self.row_hist_confirm_button.on_click(confirm)

    def run_interactive_gui(self):
        self.row_hist_input = pn.widgets.TextInput(width=100)
        self.create_row_hist_confirm_button()

        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Konfiguration des Füllers für fehlende Werte",

            main=[pn.Column(
                pn.Column(pn.WidgetBox('### Eingabe der Zeit (Anzahl der vergangenen reihen) zwischen dem fehlenden und dem neuen Wert. Wenn zum Beispiel alle Zeilen \
                                            im Datensatz minutenweise angeordnet sind und der neue Wert von vor 24 Stunden genommen wird, dann ist die Anzahl der vergangenen Zeilen 1440 (24*60)', 
                                        self.row_hist_input, width=1000),
                          pn.Column(self.row_hist_confirm_button, margin=(25, 0, 0, 0))),)
            ],
        )
        self._show_layout()
        return self.settings