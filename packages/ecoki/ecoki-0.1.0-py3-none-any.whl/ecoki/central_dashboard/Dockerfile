# Dockerfile-flask

# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:3.6
LABEL maintainer "Dennis Bode | BIBA"

# Set an environment variable with the directory
# where we'll be running the app
#ENV INIT /init

# Create the directory and instruct Docker to operate
# from there from now on
#RUN mkdir $INIT
#WORKDIR $INIT
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Expose the port uWSGI will listen on
EXPOSE 20000

# Install curl for healthcheck
#RUN apt-get update && apt-get install -y --force-yes curl unixodbc-dev apt-transport-https

# Copy the requirements file in order to install
# Python dependencies
#COPY requirements.txt .
COPY central_dashboard/requirements.txt /usr/src/app/

# Install Python dependencies
#RUN pip install -r requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Anwendung kopieren (add also files outside build context)
#COPY ./app /usr/src/app
RUN mkdir -p /usr/src/app/building_blocks
RUN mkdir -p /usr/src/app/pipelines
RUN mkdir -p /usr/src/app/central_dashboard
RUN mkdir -p /usr/src/app/framework
RUN mkdir -p /usr/src/app/energy_efficiency_scenarios
RUN mkdir -p /usr/src/app/success_story

RUN cd ..

COPY ./building_blocks /usr/src/app/building_blocks
COPY ./pipelines /usr/src/app/pipelines
COPY ./central_dashboard /usr/src/app/central_dashboard
COPY ./framework /usr/src/app/framework
COPY ./energy_efficiency_scenarios /usr/src/app/energy_efficiency_scenarios
COPY ./success_story /usr/src/app/success_story

WORKDIR /usr/src/app/central_dashboard/app
#
RUN sed -i -e 's/\r$//' prepare_app.sh
RUN chmod +x prepare_app.sh

#ENTRYPOINT ["python3"]
CMD ["./prepare_app.sh" ]


