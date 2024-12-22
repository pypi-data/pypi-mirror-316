Contributing to EcoKI
====================

Everyone is welcome to contribute to EcoKI. There are several ways to contribute:

* Report bugs or request features by opening issues
* Fix bugs or implement new features through pull requests 
* Improve documentation
* Help answer questions in discussions

How to contribute
------------------

Fork the Repository
~~~~~~~~~~~~~~~~~~~

#. Visit the EcoKI repository on GitHub
#. Click the "Fork" button in the top right 
#. Clone your fork locally:

.. code-block:: bash

    git clone git@gitlab.bik.biba.uni-bremen.de:hop/ecoki.git

Set Up Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Create and activate a Conda environment with Python 3.10:

.. code-block:: bash

    conda create -n ecoki python=3.10
    conda activate ecoki

#. Configure Poetry to use Python 3.10 (skip if Python 3.10 is your only installation):

.. code-block:: bash

    poetry env use [path to python 3.10]

#. Install dependencies using Poetry:

.. code-block:: bash

    poetry install

#. Activate the Poetry environment:

.. code-block:: bash

    poetry shell

Create a Branch
~~~~~~~~~~~~~~~

Create a branch for your changes:

.. code-block:: bash

    git checkout -b feature/my-contribution

Make Changes
~~~~~~~~~~~~

#. Make your changes following our coding guidelines
#. Add or update tests as needed
#. Update documentation if required
#. Verify all tests pass:

.. code-block:: bash

    pytest tests/

Submit Pull Request
~~~~~~~~~~~~~~~~~~~ 

#. Push changes to your fork:

.. code-block:: bash

    git push origin feature/my-contribution

#. Go to the EcoKI repository and create a Pull Request
#. Fill out the PR template with all relevant information
#. Wait for review and address any feedback

Coding Guidelines
----------------

Code Style
~~~~~~~~~~~

* Follow PEP 8 style guide
* Use meaningful variable and function names
* Add docstrings in numpy style for all functions/classes
* Keep functions focused and concise
* Use type hints where possible

Building Blocks
~~~~~~~~~~~~~~~

* Follow Building Block requirements in :doc:`requirements_new_bb`
* Implement required methods and attributes
* Include comprehensive docstrings
* Add appropriate inlet/outlet ports
* Include unit tests

Pipelines
~~~~~~~~~~

* Follow Pipeline requirements in :doc:`requirements_new_pipeline`
* Use proper JSON structure
* Document all settings and connections
* Test pipeline functionality

Testing
-------

Writing Tests
~~~~~~~~~~~~~~

* Write unit tests for all new functionality
* Use pytest as testing framework
* Place tests in appropriate test directory
* Include both positive and negative test cases
* Test edge cases and error conditions

Running Tests
~~~~~~~~~~~~~~

Run the full test suite:

.. code-block:: bash

    pytest

Run specific tests:

.. code-block:: bash

    pytest tests/path/to/test_file.py

Documentation
------------

API Documentation
~~~~~~~~~~~~~~~~~

* Use numpy doc style docstrings
* Document all parameters and return values
* Include examples where helpful
* Update API docs for new features

User Guide
~~~~~~~~~~~

* Add usage examples for new features
* Keep examples clear and concise
* Include common use cases
* Document any gotchas or limitations

Pull Request Guidelines
---------------------

PR Requirements
~~~~~~~~~~~~~~~

* Reference any related issues
* Include comprehensive description
* Add/update tests
* Update documentation
* Follow code style guidelines
* Ensure CI passes

Review Process
~~~~~~~~~~~~~~

* Maintainers will review PRs
* Address all review comments
* Keep PR scope focused
* Be responsive to feedback

Questions and Support
---------------------

* Use GitHub Discussions for general questions
* Open issues for bugs/features
* Join our community channels
* Check existing issues/discussions first

Thank you for contributing to EcoKI!
