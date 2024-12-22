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

        regex_input = pn.widgets.TextInput(
            name='Wähle den einen regular expression (regex) String, mit dem die Unterteilung der Spaltennamen in Zeitreihenzugehörigkeit vorgenommen werden kann',
            value=self.building_block.settings['regex_pattern'])

        self.layout_general = pn.Column(regex_input,pn.Spacer(width=1), styles=dict(background='LightGray'))

        # save_button callback
        def on_save_button_click(event):

            # create boundaries settings json from GUI input
            valid_boundaries = True

            # check for valid settings input
            if valid_boundaries:

                save_button.disabled = True

                # override the settings of the building block with the users input
                self.settings = self.building_block.settings
                self.settings["regex_pattern"] = regex_input.value

                # give message through GUI
                self.layout_general[-1] = pn.Column(pn.pane.Alert("Einstellungen wurden erfolgreich übernommen. Bitte fahren Sie mit der Konfiguration fort.", alert_type="success"))

                # disable
                self.disable_all_elements(self.settings_GUI)

                # set event lock
                self.event_lock.set()

            else:
                # give error message through GUI
                self.layout_general[-1],= pn.Column(pn.pane.Alert("Fehler", alert_type="danger"))

        # save_button with on click
        save_button.on_click(on_save_button_click)

        settings_general_ppl = pn.Column("## Allgemeine Einstellungen",
                                   "Hier können zusätzlich einige generelle Einstellungen vorgenommen werden.",
                                   self.layout_general, save_button)

        self.settings_GUI = pn.Column(settings_general_ppl)

        self._show_layout()

        return self.settings