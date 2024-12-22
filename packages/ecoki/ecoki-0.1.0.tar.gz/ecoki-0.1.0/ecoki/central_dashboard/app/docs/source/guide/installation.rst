Installation
============

Prerequisites
-------------

Before installing the Ecoki Central Dashboard, ensure you have the following prerequisites:

- Python 3.8 or higher
- pip (Python package installer)
- Git

Installation Steps
------------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/your-repo/ecoki-central-dashboard.git
      cd ecoki-central-dashboard

2. Set up a virtual environment (optional but recommended):

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the required dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

4. Set up the database:

   .. code-block:: bash

      python manage.py migrate

5. Create a superuser account:

   .. code-block:: bash

      python manage.py createsuperuser

6. Start the development server:

   .. code-block:: bash

      python manage.py runserver

7. Access the dashboard at `http://localhost:8000` and log in with your superuser credentials.

Configuration
-------------

To configure the Ecoki Central Dashboard, you may need to modify the following files:

- `ecoki_app/settings.py`: Main Django settings file
- `ecoki_dashboard_active/views.py`: Contains view functions for the dashboard

For more detailed configuration options, please refer to the Configuration section of this documentation.

Troubleshooting
---------------

If you encounter any issues during installation, please check the following:

1. Ensure all prerequisites are correctly installed.
2. Verify that all required environment variables are set.
3. Check the Django error logs for any specific error messages.

For further assistance, please refer to the FAQ section or contact our support team.
