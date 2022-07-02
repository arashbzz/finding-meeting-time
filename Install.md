# Docker mode
    clone the project
    docker-compose up or docker-compose up -f
    docker-compose run api sh -c "python manage.py test"
    docker-compose run api sh -c "python manage.py makemigrations"
    docker-compose run api sh -c "python manage.py migrate"

# Hosted mode
    clone the project
    install mogoDb 
    set settings for mongo db base to the database
    pip install venv env
    pip install requirements.txt
    python manage.py test"
    docker-compose run api sh -c "python manage.py make
    python python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver


URLS:
 # (for importing file to the application: )
    http://0.0.0.0:8000/meeting/
# for listing employing id:
    http://127.0.0.1:8000/meeting/employees/
# for finding free times
    http://127.0.0.1:8000/meeting/findingmeetingtime/ 
    input json example:
            {
         "employees":[48639959687376052586683994275030460621,66174599159165111158176058955002446381,156281747655501356358519480949344976171,112744177331057436352972918186353829893,192245389528611536094472390301232313501],
         "day_range": ["2015-3-20", "2015-3-20"],
         "working_hours":["07:00:00", "20:00:00"],
         "time_def":60
        }