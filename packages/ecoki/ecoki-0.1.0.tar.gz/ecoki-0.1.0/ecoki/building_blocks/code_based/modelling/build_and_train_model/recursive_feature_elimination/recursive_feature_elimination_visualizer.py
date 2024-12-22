from ecoki.visualizer_framework.visualizer import Visualizer

import panel as pn
import hvplot.pandas
import pandas as pd
import networkx as nx
import holoviews as hv
from holoviews import opts
from networkx import spring_layout
from bokeh.plotting import figure, show, output_file
from bokeh.models import BoxAnnotation, Label, LabelSet, ColumnDataSource, Arrow, OpenHead
from bokeh.io import output_notebook
from bokeh.layouts import column
from bokeh.embed import components
import graphviz
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('agg')
hv.extension('bokeh')

class TabularDataDashboard:
    """
    A class to create a dashboard for visualizing feature ranking results.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the feature ranking results.
    output_data_1 : sklearn.model_selection._search.GridSearchCV
        The GridSearchCV object containing the cross-validation results.
    df_full_rank : pandas.DataFrame
        The dataframe containing the complete feature ranking results, not just significant vs non-significant.

    Attributes
    ----------
    df : pandas.DataFrame
        The dataframe containing the feature ranking results.
    output_data_1 : sklearn.model_selection._search.GridSearchCV
        The GridSearchCV object containing the cross-validation results.
    df_full_rank : pandas.DataFrame
        The dataframe containing the complete feature ranking results, not just significant vs non-significant.

    Methods
    -------
    create_view(accent="#00A170"):
        Creates and returns a dashboard for visualizing feature ranking results.

        Parameters
        ----------
        accent : str, optional
            The color accent for the dashboard. Default is "#00A170".

        Returns
        -------
        dashboard : panel.template.MaterialTemplate
            The dashboard for visualizing feature ranking results.
    """

    def __init__(self, df, output_data_1, df_full_rank):
        """
        Initializes the TabularDataDashboard object with the given parameters.

        Parameters
        ----------
        df : pandas.DataFrame
            The dataframe containing the feature ranking results.
        output_data_1 : sklearn.model_selection._search.GridSearchCV
            The GridSearchCV object containing the cross-validation results.
        df_full_rank : pandas.DataFrame
            The dataframe containing the complete feature ranking results, not just significant vs non-significant.
        """
        self.df = df
        self.output_data_1 = output_data_1
        self.df_full_rank = df_full_rank

    def create_view(self, accent="#00A170"):
        """
        Creates and returns a dashboard for visualizing feature ranking results.

        Parameters
        ----------
        accent : str, optional
            The color accent for the dashboard. Default is "#00A170".

        Returns
        -------
        dashboard : panel.template.MaterialTemplate
            The dashboard for visualizing feature ranking results.
        """
        important_features = self.df[self.df['Feature_rank'] == 1].index.tolist()
        non_important_features = self.df[self.df['Feature_rank'] != 1].index.tolist()

        important_table = pn.pane.DataFrame(
            pd.DataFrame(important_features, columns=['Important Features']),
            name='Important features',
            width=250,
            height=400,
            index=False,  # Hide the index column
            headers=None  # Hide the column name
        )

        if non_important_features:
            non_important_table = pn.pane.DataFrame(
                pd.DataFrame(non_important_features, columns= ['Non-important Features']),
                name='Non-important features',
                width=250,
                height=400,
                index=False,  # Hide the index column
                headers=None  # Hide the column name
            )
        else:
            non_important_table = pn.pane.Markdown(
                'No non-important features found.',
                name='Non-important features',
                width=250,
                height=400
            )

        rank = self.df_full_rank[self.df_full_rank['Feature_rank'] >= 1].index.tolist()
        df_rank = pd.DataFrame(rank, columns=['Feature'])
        df_rank.index = df_rank.index + 1  # Change the index to start from 1 since this is a ranking
        rank_table = pn.pane.DataFrame(
            df_rank,
            name='Ranking of features',
            width=250,
            height=400,
            index=True,  # Show the index column
            index_header = 'Rank',
            headers=None  # Hide the column name
        )


        plt.figure(figsize=(10, 6))
        # plt.xlabel("Number of features selected")
        # plt.ylabel("Cross validation score (accuracy)")
        # plt.plot(range(1, len(self.output_data_1.cv_results_['mean_test_score'])+ 1), self.output_data_1.cv_results_['mean_test_score'])
        # plt.tight_layout()  # Improve the layout

        # Access cv_results_
        results = self.output_data_1.cv_results_

        # Calculate mean and standard deviation of cross-validated scores
        mean_scores = results['mean_test_score']
        std_scores = results['std_test_score']

        # Plotting
        plt.figure(figsize=(10, 6), dpi=300)
        plt.title('RFECV - Cross-validated performance vs. Number of Features', fontsize=14)
        plt.xlabel('Number of Features Selected', fontsize=12)
        plt.ylabel('Cross-validated Score (Accuracy)', fontsize=12)

        # Plot the mean line
        plt.plot(range(1, len(mean_scores) + 1), mean_scores, marker='o', linestyle='-', label='Mean Score')

        # Shade the area around the mean line to represent variability
        plt.fill_between(range(1, len(mean_scores) + 1),
                         mean_scores - std_scores,
                         mean_scores + std_scores,
                         alpha=0.2, label='Variability')

        # Highlight the best number of features
        plt.axvline(x=self.output_data_1.n_features_, color='black', linestyle='--',
                    label=f'Best Number of Features: {self.output_data_1.n_features_}')

        # Show legend with corresponding score
        legend = plt.legend(loc='lower right', title=f'CV Score: {round(np.max(self.output_data_1.cv_results_["mean_test_score"]), 2)}',
                            fontsize='medium')
        legend.get_title().set_fontsize('medium')
        # Adjust the legend title position to the left
        legend._legend_box.align = "left"

        # Show the plot
        plt.show()

        plot_pane = pn.pane.Matplotlib(plt.gcf(), tight=True)

        dashboard = pn.template.MaterialTemplate(
            site="ecoKI",
            title="Feature Importance Dashboard",
            main=[
                pn.Column(
                    pn.Row(
                    pn.Column(
                        '## Important Features',
                        important_table
                    ),
                    pn.Column(
                        '## Non-important Features',
                        non_important_table
                    ),
                    pn.Column(
                        '## Feature Ranking',
                        rank_table
                    )
                    ),
                    pn.Column('## Feature Ranking Plot',
                              plot_pane)
                )
            ],
            accent=accent
        )

        return dashboard

class RFEVisualizer(Visualizer):
    """
    A class for visualizing the results of recursive feature elimination.

    Inherits from Visualizer.

    Methods
    -------
    __init__(**kwarg):
        Initializes the RFEVisualizer with keyword arguments.

    run():
        Executes the visualization process.
    """

    def __init__(self, **kwarg):
        """
        Initializes the RFEVisualizer with keyword arguments.
        """
        super().__init__(**kwarg)

    def run(self):
        """
        Executes the visualization process.
        """
        self.terminate()
        df = self.input_dict['output_data']
        output_data_1 = self.input_dict['output_data_1']
        output_data_2 = self.input_dict['output_data_2']
        dashboard = TabularDataDashboard(df, output_data_1, output_data_2)
        self.visualizer = dashboard.create_view()
        self._show_visualizer()
