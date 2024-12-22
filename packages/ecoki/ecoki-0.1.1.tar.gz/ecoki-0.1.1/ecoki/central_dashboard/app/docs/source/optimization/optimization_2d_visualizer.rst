Optimization2DVisualizer
=========================

.. automodule:: ecoki.building_blocks.code_based.optimization.interpret_results.optimization_2d_visualizer.optimization_2d_visualizer
   :members:

Overview
--------

The `Optimization2DVisualizer` is a building block for visualizing 2D optimization results. This class provides functionality to create an interactive 2D plot showing model predictions for labels and ratings based on optimized parameters. It helps users understand the decision-making process of the optimization algorithm in adjusting process parameters.

Key Components
--------------

1. **Optimization2DVisualizer**: The main class that handles the visualization of 2D optimization results.
2. **Interactive Plot**: A dynamic 2D plot that allows users to explore different parameter combinations and their effects on model predictions.
3. **Data Processing**: Functionality to process and prepare input data for visualization.

Usage
-----

The Optimization2DVisualizer can be used as follows:

1. Initialize the visualizer with the required settings and data.
2. Connect the necessary input data to the inlet ports.
3. Run the visualizer to create an interactive 2D plot.
4. Analyze and explore the optimization results through the interactive interface.

Example
-------

.. code-block:: python

    from ecoki.building_blocks.code_based.optimization.interpret_results.optimization_2d_visualizer.optimization_2d_visualizer import Optimization2DVisualizer

    # Initialize the visualizer
    visualizer = Optimization2DVisualizer(settings=settings)

    # Connect input data
    visualizer.set_inlet_port_data('input_data', input_data)
    visualizer.set_inlet_port_data('input_data_split_train_test', split_data)
    visualizer.set_inlet_port_data('input_data_settings', data_settings)

    # Run the visualizer
    results = visualizer.run()

    # Access the interactive plot
    interactive_plot = results['interactive_plot']

Advanced Features
-----------------

1. **Interactive Parameter Selection**: Users can dynamically select which process parameters to display on the X and Y axes of the plot.
2. **Output Selection**: The ability to choose which model output or rating to visualize as a color-coded contour on the plot.
3. **Sample Selection**: Users can select specific samples from the test dataset to visualize, allowing for detailed analysis of individual cases.
4. **Training Data Overlay**: An option to display the parameter combinations from the training dataset, helping users understand the distribution of known good parameters.
5. **Optimization Path Visualization**: The ability to show the path taken by the optimization algorithm, from the original parameters to the optimized solution.
6. **Boundary Condition Visualization**: Visual representation of any boundary conditions or constraints applied during the optimization process.

For more detailed information on the Optimization2DVisualizer, its usage, and advanced features, please refer to the API documentation and the source code.
