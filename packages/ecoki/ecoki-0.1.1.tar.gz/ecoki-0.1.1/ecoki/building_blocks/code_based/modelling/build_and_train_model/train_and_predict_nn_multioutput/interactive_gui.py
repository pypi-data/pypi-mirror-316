# System imports
import panel as pn
import threading
from functools import partial
from math import ceil, log10
import numpy as np
import pandas as pd

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock

from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
class InteractiveGUI(AbstractInteractiveGUI):
    """user interface"""

    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.inputs_name = ["input_data"]
        #self.event_lock_1 = threading.Event()

    # function for diabling all widgets status and make it non editable
    def disable_all_elements(self, layout):
        """Rekursive Funktion, um alle Elemente in einem Panel-Layout zu deaktivieren."""
        if hasattr(layout, '__iter__'):  # Überprüfen, ob das Layout iterierbar ist
            for element in layout:
                if hasattr(element, '__iter__'):  # Wenn das Element selbst ein Layout ist
                    self.disable_all_elements(element)  # Rekursiver Aufruf
                else:
                    element.disabled = True  # Das disabled-Attribut setzen

    def run_interactive_gui(self, **kwargs):
        """
        method to start settings gui and adjust settings
        """

        # create save button widget for GUI 1
        save_button = pn.widgets.Button(name='Speichere Konfiguration des Modells und fahre mit Pipeline-Konfiguration fort', button_type='primary')

        epochs_input = pn.widgets.IntInput(
            name='Wähle die Anzahl der Epochen, die beim Training des neuronalen Netztes durchgeführt werden sollen',
            value=self.building_block.settings['epochs'], step=1, start=1,
            end=1000)

        dropout_input = pn.widgets.FloatInput(
            name='Wähle den Dropout nach jedem Layer (0 bedeutet keinen Dropout)',
            value=self.building_block.settings['dropout'], step=0.1, start=0,
            end=1)

        batch_size_input = pn.widgets.IntInput(
            name='Wähle die Batch Size, die beim Training des neuronalen Netztes verwendet werden soll',
            value=self.building_block.settings['batch_size'], step=1, start=1,
            end=1000)

        learning_rate_input = pn.widgets.FloatInput(
            name='Wähle die Learning Rate',
            value=self.building_block.settings['learning_rate'], step=0.00001, start=0.00001,
            end=0.1)

        # Erstellung des Texteingabefeld-Widgets
        dense_layer_list = self.building_block.settings['dense_layers']
        dense_layer_string = ','.join(map(str, dense_layer_list))
        dense_layers_input = pn.widgets.TextInput(name='Gib die Anzahl Anzahl der Neuronen für jeden Layer (Komma-separiert) ein. Jeder Eintrag repräsentiert einen Dense-Layer des neuronalen Netzes', value = dense_layer_string)

        self.layout_general = pn.Column(epochs_input,dense_layers_input,dropout_input,batch_size_input,learning_rate_input,pn.Spacer(width=1), styles=dict(background='LightGray'))

        # save_button callback
        def on_save_button_click(event):

            # create boundaries settings json from GUI input
            valid_boundaries = True

            try:
                # Umwandlung des Eingabe-Strings in eine Liste von Integers
                int_list = list(map(int, self.layout_general[1].value.split(',')))

                # Überprüfung jedes Werts in der Liste
                valid_integers = [x for x in int_list if 1 <= x <= 5000]
                if len(valid_integers) == len(int_list):
                    message = "Die Einstellungen wurden erfolgreich übernommen. Bitte fahren Sie mit der Konfiguration fort"
                else:
                    invalid_values = set(int_list) - set(valid_integers)
                    message = f"Ungültige Werte für die Anzahl der Neuronen pro Epoche (außerhalb von 1 bis 5000): {invalid_values}"
                    valid_boundaries = False
            except ValueError:
                message = "Fehler bei der Angabe der Anzahl der Neuronen pro Epoche: Bitte geben Sie eine Liste von ganzen Zahlen ein, getrennt durch Kommas (z.B. 50,25,10)"
                valid_boundaries = False

            # check for valid settings input
            if valid_boundaries:

                save_button.disabled = True

                # override the settings of the building block with the users input
                self.settings = self.building_block.settings
                self.settings["epochs"] = epochs_input.value
                self.settings["dropout"] = dropout_input.value
                self.settings["learning_rate"] = learning_rate_input.value
                self.settings["batch_size"] = batch_size_input.value

                # give message through GUI
                self.layout_general[-1] = pn.Column(pn.pane.Alert(message, alert_type="success"))

                # disable
                self.disable_all_elements(self.settings_GUI)

                # set event lock
                self.event_lock.set()

            else:
                # give error message through GUI
                self.layout_general[-1],= pn.Column(pn.pane.Alert(message, alert_type="danger"))

        # save_button with on click
        save_button.on_click(on_save_button_click)

        settings_general_ppl = pn.Column("## Allgemeine Einstellungen",
                                   "Hier können zusätzlich einige generelle Einstellungen vorgenommen werden.",
                                   self.layout_general, save_button)

        self.settings_GUI = pn.Column(settings_general_ppl)

        self._show_layout()

        return self.settings