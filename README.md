# About

This site is made for convenient game evaluation. I used [bootstrap](https://themewagon.com/themes/photofolio/) for the frontend. I set a goal for myself to learn as much as possible about working with Django and Python in general.

# Building

First, create a virtual environment for the project.

```bash
python -m venv venv
```

Then, install all needed dependencies by running:

```bash
pip install -r requirements.txt
```

Run the app with:

```bash
cd .\fluid\correction_fluid\
python manage.py runserver
```

Create superuser:

```bash
python manage.py createsuperuser
```

Upload games with script:

```bash
python manage.py shell
from first_app/download import game_info
game_info()
```

After importing games into db you need to migrate changes:

```bash
python manage.py makemigrations
python manage.py migrate
```