# REST_yandex
This is my result of work on the REST API project, as part of the work for the second stage of selection to the backend development school in Yandex.


### INSTALLING:
source REST_yandex/env/bin/activate   {or equivalent}

pip install -r requirements.txt

### LAUNCH TESTS:
python manage.py test tests/

### STARTING THE SERVER:
###### (NB): csrf protection off, be careful.
python manage.py runserver 0.0.0.0:8080
### STARTING THE SERVER WITH GUNICORN:
gunicorn --workers 3 --threads 3 --bind 0.0.0.0:8080 yandex_task_arxit.wsgi


### CLEAR THE DATABASE:
python manage.py migrate core zero

python manage.py migrate
