#!/bin/bash

#source ecoki.conf
#rm ecoki_dashboard_active
#ln -s $project_folder ecoki_dashboard_active
#sleep 20s


python3 central_dashboard/app/manage.py makemigrations
python3 central_dashboard/app/manage.py migrate
python3 central_dashboard/app/manage.py collectstatic -i "*.py" -i "*.pyc" --noinput --link
python3 central_dashboard/app/manage.py runserver --nostatic 0.0.0.0:20000