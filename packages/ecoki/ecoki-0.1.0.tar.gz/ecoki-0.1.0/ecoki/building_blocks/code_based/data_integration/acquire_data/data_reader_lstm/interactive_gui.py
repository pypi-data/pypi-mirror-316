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

        self.file_input = None
        self.select_time_index = None
        self.parse_cols_as_date = None
        self.file_config_confirm_button = None
        self.index_confirm_button = None
        self.target = None
        self.ip_features = None

    def create_file_confirm_button(self):
        def file_config_confirm(event):
            dataset_path = self.file_input.value[0]
            print(dataset_path)
            separator = self.col_separator.value
            if dataset_path != '':
                self.settings['dataset_path'] = dataset_path
                self.settings['col_separator'] = separator                
                cols = pd.read_csv(dataset_path, sep=separator, index_col=False, nrows=0).columns.tolist()
                self.select_time_index = pn.widgets.MultiSelect(options=cols)
                self.parse_cols_as_date = pn.widgets.TextInput(width=100)
                
                def index_confirm(event):
                    create_next_widget_box = False
                    index_col = self.select_time_index.value
                    parse_cols_as_date = self.parse_cols_as_date.value
                    if len(index_col)>1:
                        if parse_cols_as_date:
                            print(parse_cols_as_date)
                            self.settings['index_col'] = parse_cols_as_date
                            self.settings['parse_cols_as_date'] = {parse_cols_as_date: index_col}
                            self.index_confirm_button.disabled = True
                            create_next_widget_box = True
                    elif len(index_col)==1:
                        self.settings['index_col'] = index_col[0]
                        self.settings['parse_cols_as_date'] = True
                        self.index_confirm_button.disabled = True
                        create_next_widget_box = True
                    
                    if create_next_widget_box:
                        feats = [col for col in cols if col not in index_col]
                        print(feats)
                        self.target = pn.widgets.Select(name='Select target', options=feats, margin=10)
                        self.ip_features = pn.widgets.MultiSelect(name='Select input features', options=feats, margin=10)
                        
                        def features_confirm(event):
                            print(self.target.value)
                            print(self.ip_features.value)
                            self.settings['target'] = self.target.value
                            self.settings['ip_features'] = self.ip_features.value
                            self.features_confirm_button.disabled = True
                            self.event_lock.set()
                       
                        self.features_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                         width=100, align='end')
                        self.features_confirm_button.on_click(features_confirm)

                        self.settings_GUI.main[0][6] = pn.Column(pn.WidgetBox('## Merkmale auswählen', 
                                                                 self.target, 
                                                                 self.ip_features, width=350),
                                                                 pn.Column(self.features_confirm_button, margin=(25, 0, 0, 0)))
                        
                self.index_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                         width=100, align='end')
                self.index_confirm_button.on_click(index_confirm)
                self.settings_GUI.main[0][4] = pn.Column(pn.WidgetBox('## Zeitbasierte Spalte(n) für die Indizierung auswählen', self.select_time_index, 
                                                                      '### Um mehrere Spalten zu analysieren, geben Sie den Namen der resultierenden Spalte an.\
                                                                           Zum Beispiel können Datums- und Zeitspalten zu einer Datetime-Spalte zusammengefasst werden',
                                                                      self.parse_cols_as_date, width=500),
                                                         pn.Column(self.index_confirm_button, margin=(25, 0, 0, 0)))

                self.file_config_confirm_button.disabled = True

        self.file_config_confirm_button = pn.widgets.Button(name='Konfiguration Bestätigen', button_type='primary', margin=0,
                                                       width=100,
                                                       align='end')
        self.file_config_confirm_button.on_click(file_config_confirm)

    def run_interactive_gui(self):
        self.file_input = pn.widgets.FileSelector(only_files=True, margin=25) #pn.widgets.TextInput(width=250, margin=25) #pn.widgets.FileInput(accept='.csv, .txt', margin=25)
        self.col_separator = pn.widgets.Select(name='Select column seperator', options=[",", ";"], width=200, margin=10)
        self.create_file_confirm_button()

        self.settings_GUI = pn.template.MaterialTemplate(
            site="ecoKI", title="Konfiguration des Datensatzlesers",

            main=[pn.Column(
                pn.Column("# Datensatz Konfiguration", width=500),
                pn.Spacer(width=50),
                pn.Column(pn.WidgetBox('## Absoluter Pfad des Datensatzes (csv, txt). It can be placed in ecoki/datasets/ folder. \
                                           Ein Beispieldatensatz kann unter folgendem Link heruntergeladen werden: \
                                           https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption', self.file_input, self.col_separator, width=1200),
                          pn.Column(self.file_config_confirm_button, margin=(25, 0, 0, 0))), 
                pn.Spacer(width=50),
                pn.Spacer(width=50),
                pn.Spacer(width=50),
                pn.Spacer(width=50),)
            ],
        )
        self._show_layout()
        return self.settings