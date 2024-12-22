FAQs
====

This section helps users get an overview of existing FAQs and their answers.

IT Security
----------

Data Access and Storage
^^^^^^^^^^^^^^^^^^^^^^

**1. How will the company data be accessed on premise?**

EcoKI offers three options for accessing your company's data.

**2. How will the company data be accessed remotely?**

* The on-premise central database, the on-premise running ecoKI building blocks and pipelines and the central database need to be accessible remotely by the application engineers.
* This is necessary for the development, configuration and maintenance of our ecoKI-solutions.
* The connection will be established via a secure VPN-connection to the server(s), where the following services run:

  * Central database
  * Running ecoKI building blocks and pipelines

**3. How will the company data be stored off-premise?**

* For funded research projects, data will need to be stored on the servers of the partner universities. This is necessary for the researchers, so they can work with the data.
* A secure VPN connection will be used to transfer the data to the off-premise servers.
* The full data will be stored at one location. Project partners will only be able to download limited amounts of the data from this location (details to be agreed upon in project). Full access to data will only be possible via secure VPN connection.

**4. What is expected from the company in terms of data security?**

*Answers to the following questions are expected from your company, regarding data security:*

* Understanding the IT infrastructure and security measures on the SME side

  * What kind of connection options are possible?
  * How is data stored (for example on the plant side or in the cloud etc). What kind of measures are required to access the data?
  * Which virus protection software is used and what needs are to be considered when interacting with it?

* Getting the access/connection rights

  * What is the procedure for online connection?
  * What is the procedure for offline connection?

* Understanding the data policy of the SME

  * Is it allowed to store the data in off-premise ecoKI central database?
  * How can we use the data and publish results from the project (model development, success stories etc.)?
  * What kind of actions or documentation does SME expect from the ecoKI team regarding data security?

Data Usage
^^^^^^^^^

**5. How will transparency be guaranteed on where which data is used?**

* Q1 through Q3 explain where data may be used in projects done using ecoKI. To guarantee transparency on individual projects, a legally binding confidentiality agreement will be signed by all participants, clearly stating where (e.g. on/off premise, etc.) which data will be stored and used.
* Confidentiality agreement will include:

  * On which servers data will be stored
  * Which institutions will have access to data
  * How data will be accessed

**6. How will transparency be guaranteed for what the data is used for?**

*ecoKI ensures transparency regarding what the data is used for by following these key practices:*

* Involve the client in the process

  * A close collaboration is established between your company and the Application Engineer (AE) at every step of the project, including the requirements analysis step, where your company can define its data usage constraints. Additionally, the AE is required to present a detailed work plan that includes the intended use of data at any point in the project.

* Establish internal data usage transparency policy

  * Your company's requirements on the intended use of the data can be expressed as an internal data usage transparency policy that both your company and the AE have to explicitly agree upon.

* Collect necessary data only

  * By doing so, keeping track of what the data is used for becomes easier.

* Code and dataset transparency

  * To guarantee full transparency on how your company's data is used, the source code of all ecoKI's building blocks as well as the project-specific code developed by the AE, are available to your company.

Data Modeling
------------

**1. What is a data-model?**

Generally speaking, a data model is a conceptual representation of the data structures and relationships that exist within a particular domain or application. It provides a way to organize and structure data so that it can be easily managed, queried, and analyzed. Data models are used by software developers, database administrators, and data analysts to design and implement databases, data warehouses, and other data-related systems.

**2. What is the importance of data-model?**

A data model provides a visual representation of the data, its structure, and its relationships, which makes it easier for developers, analysts, and stakeholders to understand and discuss the data. It ensures that data is accurate and consistent across the entire system. This helps to prevent errors, inconsistencies, and redundancies that can occur when data is stored and managed in an ad-hoc manner.

**3. Which Database is used in ecoKI platform?**

MongoDB is used for data-storage in ecoKI. It is a source-available cross-platform document-oriented database program. Classified as a NoSQL database program, MongoDB uses JSON-like documents with optional schemas. Instead of tables, a MongoDB database stores its data in collections.

Key differences between MongoDB and SQL databases:

+----------------------+----------------------------------------+----------------------------------------+
| Aspect              | MongoDB                                 | SQL Database                           |
+======================+========================================+========================================+
| Data Model          | Document-oriented data model            | Table-based data model                 |
+----------------------+----------------------------------------+----------------------------------------+
| Schema Flexibility  | Flexible schema allows dynamic structure| Strict schema requires predefined      |
|                    |                                         | structure                              |
+----------------------+----------------------------------------+----------------------------------------+
| Scalability         | Horizontal scaling with sharding        | Vertical scaling with replication     |
+----------------------+----------------------------------------+----------------------------------------+
| Performance         | High performance for read-heavy loads   | Can degrade with complex queries      |
+----------------------+----------------------------------------+----------------------------------------+

[Content continues with Pipeline and Building Block sections...]

Pipeline
--------

**1. How can a pipeline be configured?**

Using settings.json located in the corresponding pipeline folder.

**2. What steps are needed to run the pipeline?**

1. Create the pipeline on the pipeline overview page of the central dashboard
2. Open the created pipeline in the active pipelines and run it by clicking on run pipeline or configure run pipeline button

**3. What needs to be done to send data from one building block to another w.r.t pipeline settings.json file?**

The connection attribute in settings.json defines the connection between building blocks. Users have to specify:

* Name of the source building block
* Name of the target building block
* Names of their output and input ports

**4. How can the parameters of a pipeline be modified?**

* The parameters of custom pipelines can be modified via settings.json
* ecoKI pipelines cannot be changed or overwritten
* Users must save modified ecoKI pipelines as a new custom pipeline

**5. How do I use building pipelines in combination with my own code?**

Define input and output ports for a new building block and implement the execute method with your new code.

**6. I am new to ecoKI. Is there an example pipeline illustrating the basic concepts?**

Examples of some pipelines are present in "Custom Pipelines" category on the dashboard.

**7. How to run the pipeline on Windows?**

The process is the same as on other operating systems.

Building Blocks
-------------

**1. How can the parameters of a building block be modified?**

The parameters of a building block can be set via the settings.json file where the pipeline using said building block is defined. This is done via the settings field, which consists of a dictionary whose keys (resp. values) represent the building block's parameter names (resp. values). The mapping between the values in the settings.json file and the building block parameters is defined in the execute() method of the building block.

**2. How do I run building blocks?**

Building blocks are standalone python classes with a singular purpose. There are two ways to test run a building block:

Method-1: Using ecoKI architecture
  * Create a custom pipeline including the building block with an appropriate settings.json file
  * Print results on console or create a custom visualizer building block
  * Refer to ecoki/examples/energy_monitoring/energyMonitoring.py for an example
  * Execute the pipeline via Dashboard and view results

Method-2: Python
  * Building class can be instantiated and executed locally as a python module using LocalBuildingBlockExecutor
  * Refer to ecoki/examples/execute_eocki_pipeline/ecoKIBBExectuorExamples.ipynb

**3. How do I use building blocks in combination with my own code?**

You can combine your own pre-processing code with ecoKI modelling BBs by:
* Defining a pipeline whose first step is an ecoKI data reader loading pre-processed data
* Passing data to the ecoKI modelling BB by mapping the result of the data reader
* If using a customized building block, define a pipeline that applies this building block followed by the modelling BB

**4. How to use the visualization BB example to write the visualization method of individual BB?**

To implement a customized visualizer:
* Define a new class inheriting from the ecoKI Visualizer class
* Define a run method where:
  * Data is fetched from the input dictionary
  * A Panel object (interactive dashboard) is created
  * Panel object is assigned to self.visualizer attribute
  * self._show_visualizer() method is called

The simplest Panel object would:
* Take a pandas DataFrame and call .interactive()
* Returns an interactive Panel DataFrame (requires importing hvplot.pandas)
* Allows real-time interaction with the DataFrame
* Can be transformed, filtered while plot updates automatically

[Continuing with Dashboard and Deployment sections in next part...]

Dashboard
--------

**1. How to initiate and run the dashboard application?**

The ecoKI dashboard can be started by:

* Executing "ecoki/central_dashboard/app/start_dashboard.py"
* If no custom address or port was specified, type "localhost:20000" in a browser
* The ecoKI-Dashboard login-page should appear
* Sign in with the user "ecoki_test" and password "energy2022"

.. note::
   For full functionality of the dashboard, the backend and pipeline pool needs to be available. A full documentation for how to start all required services is provided in README.md.

**2. How can we get parameters from user through the visualization class of dashboard for specific building blocks?**

To configure pipelines step by step and provide settings via the UI:

* A configuration GUI mode for running the pipelines is available
* Once you have created a pipeline under "Active pipelines", select it
* Click on the "Configure run pipeline" button
* You can now browse through the building blocks and configure them via the UI

**3. How to create a pipeline from existing pipelines?**

* Go to the navigation bar item "Pipelines"
* From the existing pipelines, select the one you want to start
* Click on "View Details"
* A page will open with additional information
* Click on "Create this pipeline"
* The pipeline should appear in the navbar item "Active pipelines"

Deployment
---------

**1. How to install ecoKI on Windows, Mac, Linux?**

Installation process consists of three main steps:

a. Download ecoKI
  * Install git if not already available (see https://git-scm.com/downloads)
  * Run in a command window / terminal::

      git clone https://gitlab.bik.biba.uni-bremen.de/hop/ecoki.git

  .. note::
     Using the ZIP download on Gitlab or a git GUI is possible but won't be supported

b. Install Docker
  * See https://docs.docker.com/engine/install/

c. Start ecoKI (it will install on first run)
  * Windows: Run "docker_start.bat"
    * You might have to start "Docker Desktop" beforehand to start the docker daemon
  * Linux / Mac: Run "docker_start.sh"

**2. How to update ecoKI?**

Follow these steps to update:

* Open a command window / terminal inside the ecoKI folder
* Run the following command to update your copy::

    git pull

* Run ecoKI as described above

In case of persisting issues / unexpected behavior:

* Force a rebuild of the environment
  * Windows: Run "docker_start_clean.bat"
  * Linux / Mac: Run "docker_start_clean.sh"

**3. Can ecoKI auto start?**

Yes, to configure auto-start:

* Open the "compose.yaml" file in the ecoKI root folder
* Change the "restart" setting:
  * Set to "always" for automatic restart
  * Set to "no" to disable
  * See https://docs.docker.com/config/containers/start-containers-automatically/#restart-policy-details for more options
* (Re)start ecoKI to apply changes
