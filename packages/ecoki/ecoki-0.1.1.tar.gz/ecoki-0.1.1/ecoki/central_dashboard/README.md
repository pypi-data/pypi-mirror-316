# Container: ecoKI central dashboard
Maintainer: Dennis Bode | BIBA (Version: 1.0.0)
## Beschreibung local

go into directory "app" and do the following steps to MANUALLY start the dashboard:

1. run "python manage.py makemigrations" 
2. then run "python manage.py migrate" 
3. Optional: Since the django internal sqlite database is not included in our git project, this will be initially created when running the migrations. For the first startup you need to set a user by running "python manage.py createsuperuser" in terminal and setting a user and password: For the ecoKI development this is proposed to be user "ecoki_test" pw "energy2022"
4. to start the app run "python manage.py runserver --nostatic 0.0.0.0:20000"

All 4 steps  is also included in start_dashboard.py. Therefore I recommend just calling this to start the dashboard.

5. go to localhost:20000 and sign in with user "ecoki_test" pw "energy2022"

Required: the RESTAPI shell needs to run on localhost port 5000 for proper working dashboard
 
 