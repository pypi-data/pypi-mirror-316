from ecoki.visualizer_framework.visualizer import Visualizer

import panel as pn
import hvplot.pandas
import panel as pn
from panel.interact import interact, fixed
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re

pn.extension()

class AsTimeseriesVisualizerVisualizer(Visualizer):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def run(self):

        self.terminate()

        df = self.input_dict["output_data"]

        # Angepasster Regex, der negative und positive Zahlen berücksichtigt
        #pattern = r'(.*)(T[\+-]\d+-)(.*)'
        pattern = self.input_dict["regex_pattern"]

        # Filtere und extrahiere die relevanten Teile des Spaltennamens
        matches = {col: re.match(pattern, col) for col in df.columns if re.search(pattern, col)}

        # Gruppiere die Spalten basierend auf dem Präfix und Suffix des Namens, ohne die Zahl
        grouped_columns = {}
        for col, match in matches.items():
            if match:
                base_name = match.group(1) + match.group(3)  # Der Spaltenname ohne die Zahl
                # Bestimmt das Vorzeichen und extrahiert die Zahl
                sign = -1 if match.group(2)[1] == '-' else 1
                number = int(re.search(r'\d+', match.group(2)).group(0))
                full_number = sign * number
                if base_name not in grouped_columns:
                    grouped_columns[base_name] = []
                grouped_columns[base_name].append((full_number, col))

        # Sortiere jede Gruppe basierend auf der extrahierten Zahl
        sorted_grouped_columns = {k: [(num, col) for num, col in sorted(v)] for k, v in grouped_columns.items()}

        self.samples = df
        self.grouped_columns = sorted_grouped_columns
        def plot_data(columns_1, columns_2, Testdaten_Index=1):

            grouped_columns = self.grouped_columns
            samples = self.samples
            Testdaten_Index = Testdaten_Index - 1

            # Erstellen des Plots
            fig, ax1 = plt.subplots()
            ax1.set_xlabel('X Daten')
            ax1.set_ylabel('Y1 Daten')

            #
            lines = []

            # plots columns for first axis
            for column_1 in columns_1:

                x_1 = [elem[0] for elem in grouped_columns[column_1]]
                y_1 = [samples.iloc[Testdaten_Index, :].loc[elem[1]] for elem in grouped_columns[column_1]]

                # Daten auf der ersten Y-Achse plotten
                line, = ax1.plot(x_1, y_1, label = column_1)  # Grüne Linie
                lines.append(line)

            # Zweite Y-Achse erstellen
            ax2 = ax1.twinx()
            ax2.set_ylabel('Y2 Daten')

            # plots columns for second axis
            for column_2 in columns_2:

                x_2 = [elem[0] for elem in grouped_columns[column_2]]
                y_2 = [samples.iloc[Testdaten_Index, :].loc[elem[1]] for elem in grouped_columns[column_2]]

                line, = ax2.plot(x_2, y_2, label = column_2)  # Blaue Linie
                lines.append(line)

            # add legend
            labels = [line.get_label() for line in lines]
            ax1.legend(lines, labels, loc='upper left')

            # Titel und Anzeigen des Plots
            plt.title('Plot mit zwei Y-Achsen')

            # set figsize
            fig = plt.gcf()
            fig.set_size_inches(12, 8)

            return fig

        # Erzeuge MultiSelect Widgets für Früchte und Gemüse
        multi_select_columns_1 = pn.widgets.MultiSelect(name='Wähle die zu plottenden Daten für die linke Y-Achse', options=list(sorted_grouped_columns.keys()), size=8)
        multi_select_columns_2 = pn.widgets.MultiSelect(name='Wähle die zu plottenden Daten für die rechte Y-Achse', options=list(sorted_grouped_columns.keys()), size=8)

        # Erzeuge einen IntSlider für die Menge
        int_slider = pn.widgets.IntSlider(name='Wähle den Index des Testdatensamples, für das du die Plots erstellen möchtest', start=1, end=len(df), step=1, value=1)
        int_input = pn.widgets.IntInput(name='Optional kann hier der Index eingegeben werden', start=1, end=len(df), step=1,value=1)

        def update_slider(event):
            int_slider.value = int(int_input.value)
        int_input.param.watch(update_slider, 'value')

        def update_input(event):
            int_input.value = int(int_slider.value)
        int_slider.param.watch(update_input, 'value')

        # Verbinde die Widgets mit der Funktion
        interactive_panel = pn.bind(plot_data, columns_1=multi_select_columns_1,
                                    columns_2=multi_select_columns_2, Testdaten_Index=int_slider)

        # set Visualizer
        self.visualizer = pn.Row(pn.Column("## Zeitreihen Plot","Die Daten können hier gemäß eines regulären Ausdrucks als Zeitreihe angezeigt werden. Die Zeitdimenseion ist auf der X-Achse aufgetragen, 0 ist dabei der aktuelle Zeitpunkt.", multi_select_columns_1, multi_select_columns_2, int_slider, int_input), interactive_panel).servable()

        # start app
        self._show_visualizer()
