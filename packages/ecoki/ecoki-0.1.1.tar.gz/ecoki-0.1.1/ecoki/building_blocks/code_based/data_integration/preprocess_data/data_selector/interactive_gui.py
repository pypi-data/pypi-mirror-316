# System imports
import pandas as pd
import panel as pn
from ecoki.interactive_gui_framework.abstract_interactive_gui import AbstractInteractiveGUI
import json


class InteractiveGUI(AbstractInteractiveGUI):
    def __init__(self, endpoint, port, building_block):
        super().__init__(endpoint, port, building_block)

        self.selected_columns = []  # gui widgets specific attribute
        self.components_checkbox = {}  # gui widgets specific attribute
        self.checkbox_list = []  # gui widgets specific attribute
        self.button = None  # gui widgets specific attribute

        self.inputs_name = ["input_data"]  # gui input name list, empty, if no input is required

        self.option_buttons = []

        self.components_checkbox = {}
        self.checkbox_list = []

        self.file_input = None

        self.select_widgets = []
        self.manual_config_tabs = pn.Tabs()
        self.file_select = pn.widgets.FileSelector('~')

        self.local_file_path_text_input = pn.Column(pn.widgets.Checkbox(name='Datensatz speichern'), pn.widgets.TextInput(name='Save dataset in local file', placeholder='Enter the file path here...',
                                                               value="ecoki/datasets/"))
        self.buttons = {}

        manual_config_button = self.create_manual_config_button()
        self.option_buttons.append(manual_config_button)

        file_config_button = self.create_file_config_button()
        self.option_buttons.append(file_config_button)

        self.if_mongoDB = False

    def create_back_button(self):

        def back_view(event):
            self.settings_GUI.main[0][0] = pn.Column("# Datensatz Konfiguration", width=500)
            self.settings_GUI.main[0][2] = pn.WidgetBox("", *self.option_buttons, width=350)

        back_button = pn.widgets.Button(name='Zurück zur Hauptseite', button_type='primary', width=300,
                                        margin=(25, 0, 0, 0),
                                        align='end')
        back_button.on_click(back_view)
        self.buttons["back"] = back_button
        return back_button

    def create_file_config_button(self):

        def file_configure(event):
            self.file_input = pn.widgets.FileInput(accept='.json', margin=25)

            file_config_confirm_button = self.create_file_confirm_button()
            back_button = self.create_back_button()

            self.settings_GUI.main[0][0] = pn.Column("# Konfigurationsdatei", width=500)
            self.settings_GUI.main[0][2] = pn.Column(pn.WidgetBox('## Datei Hochladen', self.file_input, width=350),
                                                     pn.Column(file_config_confirm_button, back_button,
                                                               margin=(25, 0, 0, 0)))

        file_config_button = pn.widgets.Button(name='Konfiguration mit Datei', button_type='primary', width=300,
                                               height=50,
                                               align='center', margin=25)
        file_config_button.on_click(file_configure)

        return file_config_button

    def create_file_confirm_button(self):
        def file_config_confirm(event):
            file_config_json = self.file_input.value
            file_config = json.loads(file_config_json)
            self.settings = file_config
            # self.buttons["file_config"].disabled = True

            for button in self.buttons.values():
                if not button.disabled:
                    button.disabled = True
            self.event_lock.set()

        file_config_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                       width=100,
                                                       align='end')
        file_config_confirm_button.on_click(file_config_confirm)
        self.buttons["file_config"] = file_config_confirm_button

        return file_config_confirm_button

    def create_manual_config_button(self):
        def manual_configure(event):
            names_list = self.inputs["input_data"].columns.tolist()
            print(names_list)

            split_list_total = []
            for column_name in names_list:
                split_list = []
                split_names = column_name.split(".")
                component_name = None
                for i in range(len(split_names)):
                    if split_names[i] in ["components", "property", "subcomponents", "value", "id"]:
                        split_list.append(split_names[i])
                    else:
                        if component_name:
                            component_name = component_name + "." + split_names[i]
                        else:
                            component_name = split_names[i]

                        if i + 1 == len(split_names):
                            split_list.append(component_name)
                            component_name = None
                        elif split_names[i+1] in ["components", "property", "subcomponents", "value", "id"]:
                            split_list.append(component_name)
                            component_name = None

                split_list_total.append(split_list)

            if not self.select_widgets:
                for i in range(len(names_list)):
                    components_column_list = pn.Column(pn.Spacer(width=100))  #pn.Spacer(width=100)
                    panel_checkbox = pn.widgets.Checkbox(name=names_list[i], width=550)
                    column_widget = pn.Column(panel_checkbox, pn.widgets.TextInput(name='Umbenennen',
                                                                                   placeholder='Enter a string here...',
                                                                                   width=550), pn.Spacer(width=20),
                                              sizing_mode='scale_width')
                    self.select_widgets.append(column_widget)
                    if names_list[i].split(".")[0] != "components":
                        components_column_list.append(column_widget)
                        self.components_checkbox[names_list[i]] = components_column_list
                    else:
                        if not self.if_mongoDB:
                            self.if_mongoDB = True

                        last_component_name = None
                        try:
                            # last_component_name = names_list[i - 1].split(".")[1]
                            last_component_name = split_list_total[i - 1][1]
                        except IndexError:
                            pass

                        if i == 0:
                            components_column_list.append(column_widget)
                            # self.components_checkbox[names_list[i].split(".")[1]] = components_column_list
                            self.components_checkbox[split_list_total[i][1]] = components_column_list
                        else:


                            if split_list_total[i][1] == last_component_name:
                                # self.components_checkbox[names_list[i].split(".")[1]].append(column_widget)
                                self.components_checkbox[split_list_total[i][1]].append(column_widget)

                            else:
                                components_column_list.append(column_widget)
                                # self.components_checkbox[names_list[i].split(".")[1]] = components_column_list
                                self.components_checkbox[split_list_total[i][1]] = components_column_list

            if not self.manual_config_tabs.objects:
                if self.if_mongoDB:
                    components_layout = pn.Tabs()  # tabs_location="left"
                    for key, value in self.components_checkbox.items():
                        components_layout.append((key, value))
                else:
                    components_layout = pn.Column()
                    for key, value in self.components_checkbox.items():
                        components_layout.append(value)

                self.manual_config_tabs.append(
                    ("Spaltenkonfiguration", pn.Row(components_layout, width=1000)))
                #self.buttons["file_path"] = self.local_file_path_text_input

                save_config = pn.Column(
                    pn.widgets.Checkbox(name=" Konfiguration in eine lokale Datei speichern"),
                    pn.widgets.TextInput(name='Dateiname', placeholder='Enter a string here...'),
                    pn.Card(self.file_select, title='Konfiguration speichern', collapsed=True, width=550))
                self.manual_config_tabs.append(("Konfiguration speichern", save_config))

            manual_config_confirm_button = self.create_manual_confirm_button()
            manual_all_columns_confirm_button = self.create_all_columns_button()
            reset_button = self.create_reset_button()
            back_button = self.create_back_button()

            if self.if_mongoDB:
                manual_numeric_values_confirm_button = self.create_numeric_values_button()
            else:
                manual_numeric_values_confirm_button = pn.Spacer(width=50)

            self.settings_GUI.main[0][0] = pn.Column("# Manuelle Konfiguration", width=500)
            self.settings_GUI.main[0][2] = pn.Row(pn.Column(self.manual_config_tabs, margin=(20, 0, 0, 0), align='end'),
                                                  pn.Spacer(width=50),
                                                  pn.Column(self.local_file_path_text_input,
                                                            manual_numeric_values_confirm_button,
                                                            manual_all_columns_confirm_button,
                                                            manual_config_confirm_button,
                                                            reset_button, back_button))

        manual_config_button = pn.widgets.Button(name='Manuelle Konfiguration', button_type='primary', width=300,
                                                 height=50, align='center', margin=25)
        manual_config_button.on_click(manual_configure)

        return manual_config_button

    def create_numeric_values_button(self):
        def select_numeric_values(event):
            for i in self.select_widgets:
                if i[0].name == "timestamp" or i[0].name.split(".")[-1] == "value":
                    # selected_columns[i[0].name] = i[1].value
                    i[0].value = True
            self.buttons["numeric_button"].disabled = True

        manual_numeric_values_confirm_button = pn.widgets.Button(name='Alle numerischen Werte auswählen',
                                                                 button_type='primary',
                                                                 margin=(25, 0, 0, 0),
                                                                 width=300,
                                                                 align='end')
        manual_numeric_values_confirm_button.on_click(select_numeric_values)
        self.buttons["numeric_button"] = manual_numeric_values_confirm_button

        return manual_numeric_values_confirm_button

    def create_all_columns_button(self):
        def select_all_columns(event):
            for i in self.select_widgets:
                i[0].value = True

            self.buttons["all_columns_button"].disabled = True

        manual_all_columns_confirm_button = pn.widgets.Button(name='Alle Spalten auswählen',
                                                              button_type='primary',
                                                              margin=(25, 0, 0, 0),
                                                              width=300,
                                                              align='end')
        manual_all_columns_confirm_button.on_click(select_all_columns)
        self.buttons["all_columns_button"] = manual_all_columns_confirm_button

        return manual_all_columns_confirm_button

    def create_manual_confirm_button(self):
        def manual_config_confirm(event):
            select_columns = {}

            for i in self.select_widgets:
                if i[0].value:
                    select_columns[i[0].name] = i[1].value

            self.settings = {"columns": select_columns}
            save_in_local = self.manual_config_tabs[1][0].value

            if_save_dataset = self.local_file_path_text_input[0].value

            if if_save_dataset:
                save_dataset_in_local = self.local_file_path_text_input[1].value

                self.settings.update({"file_path": save_dataset_in_local})

            if save_in_local:
                file_name = self.manual_config_tabs[1][1].value
                file_path = self.manual_config_tabs[1][2][0].value[0]
                config_path = file_path + "/" + file_name + ".json"

                with open(config_path, "w") as f:
                    json.dump(self.settings, f)

            for button_name, button in self.buttons.items():
                #if button_name == "file_path":
                #    pass
                #else:
                if not button.disabled:
                    button.disabled = True
            # self.buttons["confirm"].disabled = True
            self.event_lock.set()

        manual_config_confirm_button = pn.widgets.Button(name='Konfiguration bestätigen', button_type='primary',
                                                         margin=(25, 0, 0, 0),
                                                         width=300,
                                                         align='end')
        manual_config_confirm_button.on_click(manual_config_confirm)
        self.buttons["confirm"] = manual_config_confirm_button

        return manual_config_confirm_button

    def create_reset_button(self):
        def reset(event):
            for i in self.select_widgets:
                i[0].value = False
            if self.buttons["numeric_button"].disabled:
                self.buttons["numeric_button"].disabled = False

            if self.buttons["all_columns_button"].disabled:
                self.buttons["all_columns_button"].disabled = False

        manual_reset_button = pn.widgets.Button(name='Konfiguration zurücksetzen',
                                                button_type='primary',
                                                margin=(25, 0, 0, 0),
                                                width=300,
                                                align='end')
        manual_reset_button.on_click(reset)
        self.buttons["reset"] = manual_reset_button

        return manual_reset_button

    def run_interactive_gui(self):
        # self.building_block.convert_mongodb_docs_to_df(self.inputs["input_data"])

        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Konfiguration tabellarischer Daten",

            main=[pn.Column(
                pn.Column("# Datensatz Konfiguration", width=500),
                pn.Spacer(width=50),
                pn.WidgetBox("", *self.option_buttons, width=350), )

            ],
        )

        self._show_layout()
        self.settings["selected_columns"] = self.selected_columns
        return self.settings