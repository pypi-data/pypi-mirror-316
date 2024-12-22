# System imports
import panel as pn
import threading
from functools import partial
from math import ceil, log10
import numpy as np
from bokeh.models import PrintfTickFormatter
import requests

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock

import pandas as pd
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI


# determine format for the range sliders (how many ponts after comma to be displayed)
def determine_format(resolution, minimum, maximum):
    decimals = len(str(resolution).split('.')[-1]) if '.' in str(resolution) else 0
    # determine the maximum length of the integer between Min and Max
    max_length = max(len(str(int(minimum))), len(str(int(maximum))))
    # create the format by taking into account the total length and the decimal places
    return PrintfTickFormatter(format=f"%0{max_length + decimals + 1 if decimals > 0 else 0}.{decimals}f")

def get_custom_pipeline_templates():
    try:
        #TODO: replace host and port
        collected = requests.get('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/custom/overview/')
        if collected.status_code == 200:
            # parse the JSON response and retrieve the pipeline topology
            result = collected.json()["payload"]["custom_pipelines"]
    except:
        result = []
    return result
def delete_custom_pipeline(name):
    try:
        #TODO: replace host and port
        collected = requests.delete('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/?pipeline_name='+str(name)+'')
        if collected.status_code == 200:
            print("sucess")
    except:
        print("failed")

    return

def start_custom_pipeline(name):
    try:
        #TODO: replace host and port
        collected = requests.put('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/?pipeline_type=custom&pipeline_name='+str(name)+'')
        if collected.status_code == 200:
            print("sucess")
    except:
        print("failed")

    return

def myround(x, base):
    """Round to given intervals
        Parameters
        ----------
        x : numpy array
            the values to be rounded
        base : float
            the interval of values to be rounded to

        Returns
        -------
        rounded values : numpy array
        Notes
        -----
    """
    return base * np.round(x / base)


class InteractiveGUI(AbstractInteractiveGUI):
    """user interface"""

    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.inputs_name = ["input_data"]
        self.event_lock_1 = threading.Event()
        self.event_lock_inference = threading.Event()
        self.event_lock_general = threading.Event()

    def create_boundaries_layout(self, column=None, operator=None, value=None):

        # get input from port
        input_data = self.inputs['input_data']
        training_features = input_data[0]
        training_labels = input_data[2]
        training_data = pd.concat([training_features, training_labels], axis=1)

        # set options for select widgets
        operator_options = ["greater", "less"]
        column_options = list(training_data)

        # create boundary selection row (with values or without)
        select_database_url = pn.widgets.Select(name='Merkmal', options=column_options, value=column)
        text_database_name = pn.widgets.Select(name='Operator', options=operator_options, placeholder='',
                                               value=operator)
        value_database_name = pn.widgets.FloatInput(name='Wert', value=value, placeholder='')

        # add a remove button to the row
        remove_button = pn.widgets.Button(name="\U0001F5D1", width=30, height=30, button_type="danger")

        # add callback
        def remove_row_from_layout(row):
            if row in self.layout:
                self.layout.remove(row)

        remove_button_column = pn.Column(remove_button, align="end")

        # put boundaries layout together
        boundaries_layout = pn.Row(select_database_url, text_database_name, value_database_name, remove_button_column,
                                   styles=dict(background='LightGray'))

        # add callback
        remove_button.on_click(lambda event, row=boundaries_layout: remove_row_from_layout(row))

        return boundaries_layout

    def create_optimization_target_layout(self, process_parameter=None, left_bound=None, right_bound=None,
                                          exploration_radius=None, resolution=None):

        # get input from port
        input_data = self.inputs['input_data']
        training_features = input_data[0]
        training_labels = input_data[2]
        training_data = pd.concat([training_features, training_labels], axis=1)
        column_options = list(training_features) + ['']

        # check if it is in the settings
        if not process_parameter in training_data.columns:
            process_parameter = None

        # case when a new line was added and initially no selection is done
        if process_parameter is None:

            process_parameter = pn.widgets.Select(name='Prozessparameter', options=column_options, value='')
            range_slider = pn.widgets.RangeSlider(name='Grenzen für die Optimierung', start=0, end=1, value=(0, 1),
                                                  step=0.1, bar_color='#228b22')
            exploration_radius_input = pn.widgets.FloatInput(name='Explorationsradius', value=0, placeholder='',
                                                             start=0, end=1, step=0.1)
            resolution_input = pn.widgets.FloatInput(name='Auflösung/Schrittweite', value=0, placeholder='', start=0,
                                                     end=1, step=0.1)

        # for the case values are set
        else:
            min_value = training_data[process_parameter].min()
            max_value = training_data[process_parameter].max()
            exploration_radius_calc = (max_value - min_value) * 0.1
            exploration_radius_calc_rounded = myround(exploration_radius_calc, resolution)
            resolution_stepsize = 10 ** ceil(log10(resolution / 10))

            # create optimization target selection row (with values or without)
            process_parameter = pn.widgets.Select(name='Process_Parameter', options=column_options,
                                                  value=process_parameter)
            range_slider = pn.widgets.RangeSlider(name='Choose left and right bound',
                                                  start=min_value - exploration_radius,
                                                  end=max_value + exploration_radius, value=(left_bound, right_bound),
                                                  step=resolution,
                                                  format=determine_format(resolution, min_value, max_value),
                                                  bar_color='#228b22')
            exploration_radius_input = pn.widgets.FloatInput(name='Explorationsradius definieren',
                                                             value=exploration_radius, placeholder='',
                                                             start=exploration_radius_calc_rounded / 10,
                                                             end=exploration_radius_calc_rounded * 10, step=resolution)
            resolution_input = pn.widgets.FloatInput(name='Auflösung/Schrittweite definieren', value=resolution,
                                                     placeholder='', start=resolution_stepsize / 100,
                                                     end=resolution_stepsize * 1000, step=resolution_stepsize)

        # add a remove button to the row
        remove_button_2 = pn.widgets.Button(name="\U0001F5D1", width=30, height=30, button_type="danger")

        # add callback
        def remove_row_from_layout_2(row):
            if row in self.layout_2:
                self.layout_2.remove(row)

        def process_param_callback(event, row, training_data):

            # get the elected param name
            selected_parameter = row[0].value

            # calculate values for this param
            min_value = training_data[selected_parameter].min()
            max_value = training_data[selected_parameter].max()
            exploration_radius = (max_value - min_value) * 0.1
            resolution = 10 ** ceil(
                log10((training_data[selected_parameter].max() - training_data[selected_parameter].min()) / 1000))
            exploration_radius_rounded = myround(exploration_radius, resolution)
            resolution_stepsize = 10 ** ceil(log10(resolution / 10))

            # set range slider values according
            row[1].format = determine_format(resolution, myround(min_value - exploration_radius, resolution),
                                             myround(max_value + exploration_radius, resolution))
            row[1].start = myround(min_value - exploration_radius, resolution)
            row[1].end = myround(max_value + exploration_radius, resolution)
            row[1].step = resolution
            row[1].value = (myround(min_value, resolution), myround(max_value, resolution))

            # set resolution according
            row[3].start = resolution_stepsize / 100
            row[3].end = resolution_stepsize * 1000
            row[3].step = resolution_stepsize
            row[3].value = resolution

            # set exploration radius according
            row[2].start = exploration_radius_rounded / 10
            row[2].end = exploration_radius_rounded * 10
            row[2].step = resolution
            row[2].value = myround(exploration_radius, resolution)

        def resolution_input_callback(event, row, training_data):

            # prevent updates when values i reset due to changes of the start and end boundaries
            if row[3].value > row[3].start:
                if row[3].value < row[3].end:
                    # get new resolution value
                    resolution = row[3].value
                    exploration_radius = row[2].value

                    # update range slider according to the new resolution
                    row[1].format = determine_format(resolution, myround(row[1].start, resolution),
                                                     myround(row[1].end, resolution))
                    row[1].start = myround(row[1].start, resolution)
                    row[1].end = myround(row[1].end, resolution)
                    row[1].value = (myround(row[1].value[0], resolution), myround(row[1].value[1], resolution))
                    row[1].step = resolution

                    # update exploration radius according to the new resolution
                    row[2].value = myround(exploration_radius, resolution)
                    row[2].step = resolution

        def exploration_radius_input_callback(event, row, training_data):

            # get new exploration_radius value
            exploration_radius = row[2].value

            # prevent updates when values i reset due to changes of the start and end boundaries
            if exploration_radius > row[2].start:
                if exploration_radius < row[2].end:
                    # get existing resolution value
                    resolution = row[3].value

                    # round exploration_radius value by the resolution
                    rounded_exploration_radius = myround(exploration_radius, resolution)

                    # set exploration_radius to rounded value
                    row[2].value = rounded_exploration_radius

                    # get selected param name
                    selected_parameter = row[0].value

                    # reset min, max values of the range slider according to the new exploration radius
                    min_value = training_data[selected_parameter].min()
                    max_value = training_data[selected_parameter].max()
                    row[1].start = myround(min_value - rounded_exploration_radius, resolution)
                    row[1].end = myround(max_value + rounded_exploration_radius, resolution)

        # create remove button
        remove_button_column_2 = pn.Column(remove_button_2, align="end")

        # put optimization_params_layout layout together
        optimization_params_layout = pn.Row(process_parameter, range_slider, exploration_radius_input, resolution_input,
                                            remove_button_column_2, styles=dict(background='LightGray'))

        # add the callback when a different feature is selected
        process_parameter.param.watch(
            partial(process_param_callback, row=optimization_params_layout, training_data=training_data), 'value')

        # add the callback when the resolution is changed
        resolution_input.param.watch(
            partial(resolution_input_callback, row=optimization_params_layout, training_data=training_data), 'value')

        # add the callback when the exploration_radius is changed
        exploration_radius_input.param.watch(
            partial(exploration_radius_input_callback, row=optimization_params_layout, training_data=training_data),
            'value')

        # add the callback to the remove line button
        remove_button_2.on_click(lambda event, row=optimization_params_layout: remove_row_from_layout_2(row))

        return optimization_params_layout

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
        save_button = pn.widgets.Button(name='Speichere Konfiguration und fahre mit Pipeline-Konfiguration fort',
                                        button_type='primary')

        # create save button widget for GUI 2
        save_button_1 = pn.widgets.Button(name='Speichere Konfiguration und fahre mit Pipeline-Konfiguration fort',
                                          button_type='primary')

        # create save button widget for inference settings
        save_button_inference = pn.widgets.Button(name='Wähle diese Inferenz-Pipeline und fahre mit Pipeline-Konfiguration fort',
                                          button_type='primary')

        # create save button widget for general settings
        save_button_general = pn.widgets.Button(name='Speichere Einstellungen und fahre mit Pipeline-Konfiguration fort',
                                          button_type='primary')

        # get inference pipelines options
        all_custom_pipelines = get_custom_pipeline_templates()

        # filter by inference keyword
        keyword = 'inference'
        all_custom_pipelines = [string for string in all_custom_pipelines if keyword.lower() in string.lower()]
        all_custom_pipelines = list(all_custom_pipelines) + ['']

        if self.building_block.settings['prediction_pipeline_name'] in all_custom_pipelines:
            dropdown_value = self.building_block.settings['prediction_pipeline_name']
        else:
            dropdown_value = ''

        dropdown_inference = pn.widgets.Select(name='Inferenz-Pipeline', options=all_custom_pipelines, value='')
        self.layout_inference = pn.Row(dropdown_inference,pn.Spacer(width=1), styles=dict(background='LightGray'))

        # general settings section
        number_of_test_data_optimisations_input = pn.widgets.IntInput(name='Wähle Anzahl der Samples des Testdatensatz, die optmiert werden sollen', value=self.building_block.settings['number_of_test_data_optimisations'], step=1, start=1, end=len(self.inputs['input_data'][1]))
        self.layout_general = pn.Row(number_of_test_data_optimisations_input,pn.Spacer(width=1), styles=dict(background='LightGray'))

        # save_button callback
        def on_save_button_click(event):

            # create boundaries settings json from GUI input
            counter = 0
            boundary_conditions = {}
            valid_boundaries = True
            for idx in range(len(self.layout) - 2):
                if self.layout[idx][2].value is not None:
                    boundary_conditions["condition_" + str(counter)] = {"label_name": self.layout[idx][0].value,
                                                                        "operator": self.layout[idx][1].value,
                                                                        "boundary": self.layout[idx][2].value}
                else:
                    valid_boundaries = False

                counter = counter + 1

            # check for valid settings input
            if valid_boundaries:

                save_button.disabled = True

                # override the settings of the building block with the users input
                self.settings = self.building_block.settings
                self.settings["objective_function"]["boundary_conditions"] = boundary_conditions
                self.settings["objective_function"]["optimization_target"] = self.layout_optimization_target[0][0].value

                # give message through GUI
                self.layout[-1] = pn.Column(pn.pane.Alert(
                    "Die Einstellungen zur Optimierungszielfunktion wurden erfolgreich übernommen. Bitte fahren Sie mit der Konfiguration des nächsten Bausteins fort",
                    alert_type="success"))

                # disable
                self.disable_all_elements(self.settings_GUI[1])

                # set event lock
                self.event_lock.set()

            else:
                # give error message through GUI
                self.layout[-1], = pn.Column(pn.pane.Alert(
                    "Die Einstellungen zur Optimierungszielfunktion sind nicht gültig oder unvollständig. Bitte überprüfen Sie die Angaben.",
                    alert_type="danger"))

        # button_1 callback
        def on_save_button_click_1(event):

            valid_boundaries = True

            # create boundaries settings json from GUI input
            optimisation_parameters = {}
            for idx in range(len(self.layout_2) - 2):

                if self.layout_2[idx][0].value in optimisation_parameters.keys():
                    valid_boundaries = False

                optimisation_parameters[self.layout_2[idx][0].value] = {"left_bound": self.layout_2[idx][1].value[0],
                                                                        "right_bound": self.layout_2[idx][1].value[1],
                                                                        "exploration_radius": self.layout_2[idx][
                                                                            2].value,
                                                                        "resolution": self.layout_2[idx][3].value}

                if (self.layout_2[idx][0].value == ''):
                    valid_boundaries = False

            if valid_boundaries:

                save_button_1.disabled = True

                # override the settings of the building block with the users input
                self.settings = self.building_block.settings
                self.settings["optimisation_parameters"] = optimisation_parameters

                # give message through GUI
                self.layout_2[-1] = pn.Column(pn.pane.Alert(
                    "Die Einstellungen zur Optimierungszielfunktion wurden erfolgreich übernommen. Bitte fahren Sie mit der Konfiguration des nächsten Bausteins fort",
                    alert_type="success"))

                # disable
                self.disable_all_elements(self.settings_GUI[2])

                # set event lock
                self.event_lock_1.set()

            else:
                self.layout_2[-1] = pn.Column(pn.pane.Alert(
                    "Die Einstellungen zu den Prozessparametern sind nicht gültig oder unvollständig. Bitte überprüfen Sie die Angaben.",
                    alert_type="danger"))


        def on_save_button_inference(event):

            # if placeholder, give error message
            if dropdown_inference.value == '':
                valid = False
            else:
                valid = True

            # # if already existing, stop first
            # if save_button_inference.value in self.pipeline_manager.pipelines.keys():
            #     delete_custom_pipeline(self.settings['prediction_pipeline_name'])
            #
            # # start it
            # start_custom_pipeline(self.settings['prediction_pipeline_name'])

            if valid:

                save_button_inference.disabled = True

                # override the settings of the building block with the users input
                self.settings = self.building_block.settings
                self.settings["prediction_pipeline_name"] = dropdown_inference.value

                # give message through GUI
                self.layout_inference[-1] = pn.Column(pn.pane.Alert(
                    "Die Auswahl der Inferenz-Pipeline wurde erfolgreich übernommen. Bitte fahren Sie mit der Konfiguration fort",
                    alert_type="success"))

                # disable
                dropdown_inference.disabled = True

                # set event lock
                self.event_lock_inference.set()

            else:
                self.layout_inference[-1] = pn.Column(pn.pane.Alert(
                    "Bitte wählen Sie eine gültige Inferenz-Pipeline aus",
                    alert_type="danger"))

        def on_save_button_general(event):

            valid=True

            if valid:

                save_button_general.disabled = True

                # override the settings of the building block with the users input
                self.settings = self.building_block.settings
                self.settings["number_of_test_data_optimisations"] = number_of_test_data_optimisations_input.value

                # give message through GUI
                self.layout_general[-1] = pn.Column(pn.pane.Alert(
                    "Die Konfiguration  wurde erfolgreich übernommen. Bitte fahren Sie mit der Konfiguration fort",
                    alert_type="success"))

                # disable
                number_of_test_data_optimisations_input.disabled = True

                # set event lock
                self.event_lock_general.set()

            else:
                self.layout_general[-1] = pn.Column(pn.pane.Alert(
                    "Fehler",
                    alert_type="danger"))

        # save_button with on click
        save_button.on_click(on_save_button_click)

        # save_button with on click
        save_button_1.on_click(on_save_button_click_1)

        # save_button with on click
        save_button_inference.on_click(on_save_button_inference)

        # save_button with on click
        save_button_general.on_click(on_save_button_general)

        # button to add lines to the boundary section
        add_button = pn.widgets.Button(name="Zeile hinzufügen")

        # button to add lines to the boundary section
        add_button_2 = pn.widgets.Button(name="Prozessparameter hinzufügen")

        # Switch for advanced configuration mode
        checkbox = pn.widgets.Checkbox(name='Auflösung und Explorationsradius manuell konfigurieren', value=False)

        # add_button callback
        def add_row_to_layout(event):
            new_row = self.create_boundaries_layout()
            self.layout.insert(-2, new_row)

        add_button.on_click(add_row_to_layout)

        # add_button_2 callback
        def add_row_to_layout_2(checkbox_value):
            new_row = self.create_optimization_target_layout()
            self.layout_2.insert(-2, new_row)

            for i in range(len(self.layout_2) - 2):
                self.layout_2[i][2].disabled = not checkbox_value
                self.layout_2[i][3].disabled = not checkbox_value

        add_button_2.on_click(lambda event: add_row_to_layout_2(checkbox_value=checkbox.value))

        # create the initial layout
        self.layout = pn.Column(
            pn.Column(add_button),
            pn.Column()
        )

        # create the initial layout_2
        self.layout_2 = pn.Column(pn.Row(add_button_2, checkbox), pn.Column())

        # checkbox callback
        def checkbox_callback(event, layout):

            checkbox_value = layout[-2][1].value
            for i in range(len(layout) - 2):
                layout[i][2].disabled = not checkbox_value
                layout[i][3].disabled = not checkbox_value

        # callback when the checkbox for advanced settings is checked or unchecked
        checkbox.param.watch(partial(checkbox_callback, layout=self.layout_2), 'value')

        # get input port values
        input_data = self.inputs['input_data']
        training_features = input_data[0]
        training_labels = input_data[2]

        # widget for selecting the minimisation target
        self.layout_optimization_target = pn.Column(
            pn.Row(pn.widgets.Select(name='Wählen Sie das zu minimierende Merkmal aus:', options=list(training_labels),
                                     value=""))
        )

        # init the GUI with the existing settings
        for condition, condition_value in self.building_block.settings['objective_function'][
            'boundary_conditions'].items():
            self.layout.insert(0, self.create_boundaries_layout(column=condition_value["label_name"],
                                                                operator=condition_value["operator"],
                                                                value=condition_value["boundary"]))

        for process_param_name, process_param_values in self.building_block.settings['optimisation_parameters'].items():
            self.layout_2.insert(0, self.create_optimization_target_layout(process_parameter=process_param_name,
                                                                           left_bound=process_param_values[
                                                                               "left_bound"],
                                                                           right_bound=process_param_values[
                                                                               "right_bound"],
                                                                           exploration_radius=process_param_values[
                                                                               "exploration_radius"],
                                                                           resolution=process_param_values[
                                                                               "resolution"]))

        # set initial entries to disabled
        for i in range(len(self.layout_2) - 2):
            self.layout_2[i][2].disabled = True
            self.layout_2[i][3].disabled = True

        if self.building_block.settings['objective_function']['optimization_target'] in list(training_labels):
            self.layout_optimization_target[0][0].value = self.building_block.settings['objective_function'][
                'optimization_target']

        # build layout and start settings GUI
        settings_inference_ppl = pn.Column("## Auswahl des Modells",
                                   "Im ersten Schritt muss die Pipeline ausgewählt werden, die für das trainierte Modell eine Modell-Prediction bereitstellt. Diese Art von Pipeline wird auch Inferenz-Pipeline genannt. Im folgenden Dropdown erhalten Sie eine Auswahl aller Custom-Pipelines, die 'inference' im Namen beinhalten. Wählen Sie die entsprechende Pipeline aus und klicken Sie auf den Button.",
                                   self.layout_inference, save_button_inference)

        # build layout and start settings GUI
        settings_GUI_1 = pn.Column("## Konfiguration der Optimierungs-Zielfunktion",
                                   "Zunächst einmal muss das Qualitätsmerkmal gewählt werden, dessen Wert im Rahmen der Optimierung minimiert werden soll.",
                                   self.layout_optimization_target,
                                   "Im zweiten Schritt können Sie hier beliebig viele Randbedingungen für die Merkmale definieren.",
                                   self.layout, save_button)

        settings_GUI_2 = pn.Column("## Konfiguration der Prozessparameter",
                                   "In diesem Schritt müssen die Grenzen der Prozessparameter festgelegt werden, in denen der Optimierer eine Veränderung vornehmen darf, um die ausgewählte Zielgröße unter Einhaltung der definierten Randbedingungen zu minimieren. Über den Button 'Prozessparameter hinzufügen' können Sie in einer neuen Zeile einen Prozessparameter aus den verwendeten Features des ML-Prozessmodells auswählen. Über einen Slider können die Grenzen dieses Parameters für die Optimierung eingestellt werden. Initial stehen diese auf den Minimum- und Maximum-Werten, die im Trainingsdatensatz des Modells aufgetreten sind. Der 'Explorationsradius' gibt an, in welchem Abstand vom Parameterwert sich mindestens N Trainingsbeispiele befinden müssen. Es wird dadurch also verhindert, dass sich die Parameterwahl des Optimierers zu weit von bereits bekannten Parameterwerten entfernt befindet. Die Anzahl N kann über 'optimisation_neighbours' in den Settings eingestellt werden.  Initial wird der Explorationsradius auf 10% der Min-Max-Range eingestellt und muss somit nicht verändert werden. Ebenso wird automatisiert eine sinnvolle Auflösung/Schrittweite (in Zehnerpotenzen) ermittelt. Wichtiger Hinweis: Möchten Sie diese Werte dennoch gerne manuell konfigurieren, ist die über das Anwählen von 'Auflösung und Explorationsradius manuell konfigurieren' möglich. Dies wird jedoch nur für erfahrene Benutzer empfohlen. In einigen Fällen wie beispielseweise der Einbeziehung von Boolean-Flags (entweder 0 oder 1) ist eine Ausweitung des Explorationsradius jedoch notwendig.",
                                   self.layout_2, save_button_1)

        settings_general_ppl = pn.Column("## Allgemeine Einstellungen",
                                   "Hier können zusätzlich einige generelle Einstellungen vorgenommen werden.",
                                   self.layout_general, save_button_general)

        self.settings_GUI = pn.Column(settings_inference_ppl,settings_GUI_1, settings_GUI_2, settings_general_ppl)
        self._show_layout()
        self.event_lock_1.wait()
        self.event_lock_inference.wait()
        self.event_lock_general.wait()

        return self.settings