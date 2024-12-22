
Process Parameter Optimizer
===========================

The Process Parameter Optimizer is a sophisticated building block designed to optimize process parameters based on a trained model and given constraints. It is a key component of the optimization module in the EcoKI framework.

.. automodule:: ecoki.building_blocks.code_based.optimization.run_optimization.process_parameter_optimizer.process_parameter_optimizer
   :members:

Key Features
------------

1. Optimization of process parameters for a given sample or batch of samples.
2. Support for both continuous and discrete process parameters.
3. Utilizes differential evolution algorithm for optimization.
4. Incorporates confidence radius and ball tree for efficient nearest neighbor search.
5. Provides visualization of optimization results.
6. Handles multiple optimization strategies and constraints.
7. Integrates with various machine learning models, including XGBoost.

Core Components
---------------

1. **ProcessParameterOptimizer**: The main class that orchestrates the entire optimization process.
2. **BIKScaledBallTree**: A custom implementation of the Ball Tree algorithm for efficient nearest neighbor search, adapted for the specific needs of the optimizer.
3. **differential_evolution_adapted**: A modified version of the differential evolution algorithm, tailored for process parameter optimization.

Key Methods
-----------

1. **train**: Prepares the model and data for optimization.
2. **run**: Executes the optimization process on the prepared data.
3. **optimize_batch**: Optimizes parameters for a batch of samples.
4. **optimize_sample**: Optimizes parameters for a single sample.
5. **predict**: Makes predictions using the trained model.
6. **objective_function**: Evaluates the quality of optimized parameters.

Usage
-----

The Process Parameter Optimizer can be used as follows:

1. Initialize the optimizer with the required settings and data.
2. Train the model using the provided training data.
3. Optimize process parameters for a single sample or a batch of samples.
4. Analyze and visualize the optimization results.

Example
-------

.. code-block:: python

    from ecoki.building_blocks.code_based.optimization.run_optimization.process_parameter_optimizer.process_parameter_optimizer import ProcessParameterOptimizer

    # Initialize the optimizer
    optimizer = ProcessParameterOptimizer(settings=settings)

    # Train the model
    optimizer.train(input_data)

    # Optimize process parameters
    results = optimizer.run()

    # Access optimized parameters and predictions
    optimized_parameters = results['output_data']
    predictions = results['output_data_split_train_test']

Advanced Features
-----------------

1. **Confidence Radius**: Implements a confidence radius mechanism to ensure that optimized parameters are within a realistic range of known good parameters.

2. **Discrete Parameter Handling**: Capable of handling both continuous and discrete process parameters, using a combination of differential evolution and grid search techniques.

3. **Multi-objective Optimization**: Supports optimization of multiple objectives simultaneously, allowing for trade-offs between different performance metrics.

4. **Adaptive Optimization**: Utilizes machine learning models (such as XGBoost) to guide the optimization process, adapting to complex relationships between parameters and outcomes.

5. **Visualization Tools**: Includes built-in visualization capabilities for analyzing optimization results, including parameter importance and optimization trajectories.

Dependencies
------------

The Process Parameter Optimizer relies on several key dependencies:

- XGBoost: For building and using gradient boosting models.
- Scikit-learn: For various machine learning utilities and metrics.
- Pandas and NumPy: For data manipulation and numerical operations.
- SciPy: For optimization algorithms, including differential evolution.

For a complete list of dependencies and their versions, please refer to the project's requirements file.

For more detailed information on each component, its usage, and advanced features, please refer to the API documentation and the source code in the `ecoki/building_blocks/code_based/optimization/run_optimization/process_parameter_optimizer` directory.




