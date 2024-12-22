# System imports
import pandas as pd
import panel as pn
import threading
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
import io

pn.config.notifications = True


class InteractiveGUI(AbstractInteractiveGUI):
    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.nn_complexity_input = None
        self.nn_complexity_input_confirm_button = None

    def create_nn_complexity_input_confirm_button(self):
        def confirm(event):
            nn_complexity = self.nn_complexity_input.value
            self.settings['nn_complexity'] = nn_complexity
            self.nn_complexity_input_confirm_button.disabled = True
            self.event_lock.set()

        self.nn_complexity_input_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                                    width=100, align='end')
        self.nn_complexity_input_confirm_button.on_click(confirm)

    def run_interactive_gui(self):
        self.nn_complexity_input = pn.widgets.Select(options=["Basic"], margin=10, width=100)
        self.create_nn_complexity_input_confirm_button()

        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Auswahl der Architektur des neuronalen Netzes",

            main=[pn.Column(
                pn.Column(pn.WidgetBox('### Wählen Sie die Komplexität des für Ihre Daten verwendeten neuronalen Netzwerkmodells. \
                                            Komplexität bedeutet die Anzahl der Schichten, der Einheiten, der Epochen usw. \
                                            Zurzeit ist nur die Basisoption verfügbar. Bei dieser Option verwendet ein Keras-basiertes \
                                            neuronales Netzwerk zwei versteckte Schichten. Die erste versteckte Schicht ist LSTM mit 50 Einheiten \
                                            und die zweite Schicht ist Dense mit 25 Einheiten. Beide Schichten verwenden die Aktivierungsfunktion Relu. \
                                            Die verwendete Verlustfunktion ist mse und der Optimierer ist adam. Epochen und Batchgröße sind auf 20 \
                                            bzw. 6 eingestellt. Weitere Optionen werden in Zukunft hinzugefügt, z.B. komplexere neuronale Netzwerkarchitekturen(mittel, fortgeschritten) \
                                            und auch die Möglichkeit, Ihren eigenen Trainingscode für neuronale Netzwerke hochzuladen', 
                                        self.nn_complexity_input, width=1000),
                          pn.Column(self.nn_complexity_input_confirm_button, margin=(25, 0, 0, 0))), 
                pn.Spacer(width=50),
                pn.Spacer(width=50),)
            ],
        )
        self._show_layout()
        return self.settings