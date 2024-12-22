# System imports
import panel as pn
import threading
from functools import partial
from math import ceil, log10
import numpy as np
import pandas as pd
from bokeh.models import PrintfTickFormatter

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock

from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI

class InteractiveGUI(AbstractInteractiveGUI):
    """user interface"""

    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.inputs_name = ["input_data"]
        self.event_lock_1 = threading.Event()

    def create_feature_aggregations_layout(self, aggregation_name = None, aggregated_columns = None, aggregation_function=None, inverse_aggregation=None):

        # get input from port
        input_data = self.inputs['input_data']
        training_features = input_data[0]

        # set options for the widgets
        aggregated_columns_options = list(training_features)
        aggregation_function_options = ["mean", "median", "max"]
        inverse_aggregation_options = ["const"]

        if aggregated_columns is not None:
            aggregated_columns = [element for element in aggregated_columns if element in list(training_features)]

        if aggregation_name is None:
            aggregation_name = ""

        if aggregated_columns is None:
            aggregated_columns = []

        if aggregation_function is None:
            aggregation_function = aggregation_function_options[0]

        if inverse_aggregation is None:
            inverse_aggregation = inverse_aggregation_options[0]

        # create boundary selection row (with values or without)
        aggregation_name_widget = pn.widgets.TextInput(name='Name des neu aggregierten Features', placeholder='', value = aggregation_name)
        aggregated_columns_widget = pn.widgets.MultiSelect(name='Wähle zu aggregierende Features', value=aggregated_columns, options=aggregated_columns_options, size=10) # Alternative: MultiChoice
        aggregation_function_widget = pn.widgets.Select(name='Wähle die Aggregatsfunktion', options=aggregation_function_options, value = aggregation_function)
        inverse_aggregation_widget = pn.widgets.Select(name='Wähle die inverse Aggregatsfunktion', options=inverse_aggregation_options, placeholder='', value = inverse_aggregation)

        # add a remove button to the row
        remove_button = pn.widgets.Button(name="\U0001F5D1",width=30, height=30, button_type="danger")

        #add callback
        def remove_row_from_layout(row):
           if row in self.layout:
               self.layout.remove(row)

        remove_button_column = pn.Column(remove_button, align="end")

        # put layout together
        feature_aggregations_layout = pn.Row(aggregation_name_widget, aggregated_columns_widget, aggregation_function_widget, inverse_aggregation_widget, remove_button_column,styles=dict(background='LightGray'))

        # add callback
        remove_button.on_click(lambda event, row=feature_aggregations_layout: remove_row_from_layout(row))

        return feature_aggregations_layout
    
    def create_label_aggregations_layout(self, aggregation_name = None, aggregated_columns = None, aggregation_function=None, inverse_aggregation=None):

        # get input from port
        input_data = self.inputs['input_data']
        training_labels = input_data[2]

        # set options for the widgets
        aggregated_columns_options = list(training_labels)
        aggregation_function_options = ["mean", "median", "max"]
        inverse_aggregation_options = ["const"]

        if aggregated_columns is not None:
            aggregated_columns = [element for element in aggregated_columns if element in list(training_labels)]

        if aggregation_name is None:
            aggregation_name = ""

        if aggregated_columns is None:
            aggregated_columns = []

        if aggregation_function is None:
            aggregation_function = aggregation_function_options[0]

        if inverse_aggregation is None:
            inverse_aggregation = inverse_aggregation_options[0]

        # create boundary selection row (with values or without)
        aggregation_name_widget = pn.widgets.TextInput(name='Name des neu aggregierten Labels', placeholder='', value = aggregation_name)
        aggregated_columns_widget = pn.widgets.MultiSelect(name='Wähle zu aggregierende Labels', value=aggregated_columns, options=aggregated_columns_options, size=10) # Alternative: MultiChoice
        aggregation_function_widget = pn.widgets.Select(name='Wähle die Aggregatsfunktion', options=aggregation_function_options, value = aggregation_function)
        inverse_aggregation_widget = pn.widgets.Select(name='Wähle die inverse Aggregatsfunktion', options=inverse_aggregation_options, placeholder='', value = inverse_aggregation)

        # add a remove button to the row
        remove_button = pn.widgets.Button(name="\U0001F5D1",width=30, height=30, button_type="danger")

        #add callback
        def remove_row_from_layout(row):
           if row in self.layout_2:
               self.layout_2.remove(row)

        remove_button_column = pn.Column(remove_button, align="end")

        # put layout together
        label_aggregations_layout = pn.Row(aggregation_name_widget, aggregated_columns_widget, aggregation_function_widget, inverse_aggregation_widget, remove_button_column,styles=dict(background='LightGray'))

        # add callback
        remove_button.on_click(lambda event, row=label_aggregations_layout: remove_row_from_layout(row))

        return label_aggregations_layout
    
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
        save_button = pn.widgets.Button(name='Speichere Konfiguration der aggregierten Features und fahre mit Pipeline-Konfiguration fort', button_type='primary')

        # create save button widget for GUI 1
        save_button_2 = pn.widgets.Button(name='Speichere Konfiguration der aggregierten Labels und fahre mit Pipeline-Konfiguration fort', button_type='primary')

        # save_button callback
        def on_save_button_click(event):

            # create boundaries settings json from GUI input
            counter = 0
            feature_aggregations = {}
            valid_boundaries = True
            for idx in range(len(self.layout)-2):
                # check for empty list and string
                if self.layout[idx][0].value is not "" and len(self.layout[idx][1].value)>0:
                    # check for duplicates
                    if self.layout[idx][0].value in feature_aggregations.keys():
                        valid_boundaries = False

                    feature_aggregations[self.layout[idx][0].value] = {"aggregated_columns":self.layout[idx][1].value,"aggregation_function":self.layout[idx][2].value,"inverse_aggregation":self.layout[idx][3].value}

                else:
                    valid_boundaries = False

                counter = counter+1

            # check for valid settings input
            if valid_boundaries:

                save_button.disabled = True

                # override the settings of the building block with the users input
                self.settings = self.building_block.settings
                self.settings["feature_aggregations"] = feature_aggregations

                # give message through GUI
                self.layout[-1] = pn.Column(pn.pane.Alert("Die Einstellungen zu den Feature-Aggregationen wurden erfolgreich übernommen. Bitte fahren Sie mit der Konfiguration fort", alert_type="success"))

                # disable
                self.disable_all_elements(self.settings_GUI[0])

                # set event lock
                self.event_lock.set()

            else:
                # give error message through GUI
                self.layout[-1],= pn.Column(pn.pane.Alert("Die Einstellungen zur Feature-Aggregation sind nicht gültig oder unvollständig. Bitte überprüfen Sie die Angaben, insbesondere auf leere Felder oder Duplikate in der Benennung", alert_type="danger"))

        def on_save_button_click_2(event):

            # create boundaries settings json from GUI input
            counter = 0
            label_aggregations = {}
            valid_boundaries = True
            for idx in range(len(self.layout_2)-2):
                # check for empty list and string
                if self.layout_2[idx][0].value is not "" and len(self.layout_2[idx][1].value)>0:

                    # check for duplicates
                    if self.layout_2[idx][0].value in label_aggregations.keys():
                        valid_boundaries = False

                    label_aggregations[self.layout_2[idx][0].value] = {
                        "aggregated_columns": self.layout_2[idx][1].value,
                        "aggregation_function": self.layout_2[idx][2].value,
                        "inverse_aggregation": self.layout_2[idx][3].value}

                else:
                    valid_boundaries = False

                counter = counter+1

            # check for valid settings input
            if valid_boundaries:

                save_button_2.disabled = True

                # override the settings of the building block with the users input
                self.settings = self.building_block.settings
                self.settings["label_aggregations"] = label_aggregations

                # give message through GUI
                self.layout_2[-1] = pn.Column(pn.pane.Alert("Die Einstellungen zu den Label-Aggregationen wurden erfolgreich übernommen. Bitte fahren Sie mit der Konfiguration fort", alert_type="success"))

                # disable
                self.disable_all_elements(self.settings_GUI[1])

                # set event lock
                self.event_lock_1.set()

            else:
                # give error message through GUI
                self.layout_2[-1],= pn.Column(pn.pane.Alert("Die Einstellungen zur Label-Aggregation sind nicht gültig oder unvollständig. Bitte überprüfen Sie die Angaben, insbesondere auf leere Felder oder Duplikate in der Benennung", alert_type="danger"))

        # save_button with on click
        save_button.on_click(on_save_button_click)

        save_button_2.on_click(on_save_button_click_2)

        # button to add lines to the boundary section
        add_button = pn.widgets.Button(name="Zeile hinzufügen")

        add_button_2 = pn.widgets.Button(name="Zeile hinzufügen")

        # add_button callback
        def add_row_to_layout(event):
            new_row = self.create_feature_aggregations_layout()
            self.layout.insert(-2, new_row)

        def add_row_to_layout_2(event):
            new_row = self.create_label_aggregations_layout()
            self.layout_2.insert(-2, new_row)

        add_button.on_click(add_row_to_layout)

        add_button_2.on_click(add_row_to_layout_2)

        # create the initial layout
        self.layout = pn.Column(
            pn.Column(add_button),
            pn.Column()
        )

        # create the initial layout
        self.layout_2 = pn.Column(
            pn.Column(add_button_2),
            pn.Column()
        )

        # get input port values
        input_data = self.inputs['input_data']
        training_features = input_data[0]
        training_labels = input_data[2]

        # init the GUI with the existing settings
        for condition,condition_value in self.building_block.settings['feature_aggregations'].items():
            self.layout.insert(0, self.create_feature_aggregations_layout(aggregation_name = condition, aggregated_columns = condition_value["aggregated_columns"], aggregation_function=condition_value["aggregation_function"], inverse_aggregation=condition_value["inverse_aggregation"]))
            #aggregation_name = None, aggregated_columns = None, aggregation_function = None, inverse_aggregation = None):

        for condition, condition_value in self.building_block.settings['label_aggregations'].items():
            self.layout_2.insert(0, self.create_label_aggregations_layout(aggregation_name=condition,
                                                                          aggregated_columns=condition_value[
                                                                              "aggregated_columns"],
                                                                          aggregation_function=condition_value[
                                                                              "aggregation_function"],
                                                                          inverse_aggregation=condition_value[
                                                                              "inverse_aggregation"]))

        # build layout and start settings GUI
        settings_GUI_1 = pn.Column("## Konfiguration der Feature-Aggregationen","Hier können Sie eine Konfiguration vornehmen, sodass mehrere Features zu einem Feature zusammengefasst bzw. aggregiert werden können. Dazu müssen Sie zunächst einen Namen für das aggregierte Feature vergeben. Nachfolgend können Sie im Auswahlfenster die Features auswählen, die für die Aggregierung verwendet werden sollen. Zum Schluss müssen Sie noch die Aggregatsfunktion bestimmen, mit der das neue Feature basierend auf den ausgewählten Features berechnet wird. Es stehen der Mittelwert ('mean'), der Median ('median') oder das Maximum ('max') zur Verfügung. Im letzten Schritt kann die inverse Aggregation bestimmt werden. Hier steht aktuell nur die Möglichkeit zur Verfügung, den Wert als Konstante auf alle aggregierten Features zu übertragen. Sie können über 'Zeile hinzufügen' beliebig viele Aggregationen vornehmen.", self.layout, save_button)

        settings_GUI_2 = pn.Column("## Konfiguration der Label-Aggregationen","Hier können Sie eine Konfiguration vornehmen, sodass mehrere Labels zu einem Label zusammengefasst bzw. aggregiert werden können. Dazu müssen Sie zunächst einen Namen für das aggregierte Label vergeben. Nachfolgend können Sie im Auswahlfenster die Labels auswählen, die für die Aggregierung verwendet werden sollen. Zum Schluss müssen Sie noch die Aggregatsfunktion bestimmen, mit der das neue Label basierend auf den ausgewählten Labels berechnet wird. Es stehen der Mittelwert ('mean'), der Median ('median') oder das Maximum ('max') zur Verfügung. Im letzten Schritt kann die inverse Aggregation bestimmt werden. Hier steht aktuell nur die Möglichkeit zur Verfügung, den Wert als Konstante auf alle aggregierten Labels zu übertragen. Sie können über 'Zeile hinzufügen' beliebig viele Aggregationen vornehmen.", self.layout_2, save_button_2 )

        self.settings_GUI = pn.Column(settings_GUI_1,settings_GUI_2)
        self._show_layout()
        self.event_lock_1.wait()

        return self.settings