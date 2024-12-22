Installation
============

Features
--------

* ``ecoKI`` is an online platform with the goal of enabling a low-threshold and rapid introduction of AI to increase energy efficiency in production.
* ``ecoKI`` provides tools, knowledge and infrastructure for the use of digitalization and AI in a user-friendly way.
* ``ecoKI`` contributes networking opportunities with professionals and AI experts.

Prerequisites
-------------

Before installing ecoKI, ensure you have the following prerequisites:

1. Install Conda from https://docs.conda.io/en/latest/miniconda.html

2. Install Graphviz from https://graphviz.org/download/ (make sure to add to "Path" during installation)

3. Install Poetry from https://python-poetry.org/docs/

Installation Steps
------------------

1. Create and activate a Conda environment with Python 3.10:

   .. code-block:: bash

      conda create -n ecoki python=3.10
      conda activate ecoki

2. Clone the repository:

   .. code-block:: bash

      git clone https://gitlab.bik.biba.uni-bremen.de/hop/ecoki.git -b develop
      cd ecoki

3. Configure Poetry to use Python 3.10 (skip if Python 3.10 is your only installation):

   .. code-block:: bash

      poetry env use [path to python 3.10]

4. Install dependencies using Poetry:

   .. code-block:: bash

      poetry install

5. Activate the Poetry environment:

   .. code-block:: bash

      poetry shell

Now the correct virtual environment is activated and ecoKI is ready to use.

Troubleshooting
---------------

If you encounter any issues during installation, please check the following:

1. Ensure all prerequisites (Conda, Graphviz, Poetry) are correctly installed
2. Verify Python 3.10 is being used (check with ``python --version``)
3. Make sure Graphviz is added to your system PATH

For further assistance, please refer to the FAQ section or contact our support team.
