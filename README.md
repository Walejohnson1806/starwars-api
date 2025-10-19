# Starwars films API

A Django REST API for managing Star Wars films and user comments, with data sourced from SWAPI.

# Features

- get list of Star Wars films sorted by release date
- View detailed information about each film
- Add comments to films (max 500 characters)
- List comments for each film in chronological order
- Automatic data sync from SWAPI
- interactive API documentation (swagger UI)

# API Endpoints

# Films
- `GET /api/films/` - List all films with comment counts
- `GET /api/films/{id}/` - Get detailed film information
- `POST /api/films/sync/` - Sync films from SWAPI

### Comments
- `GET /api/films/{film_id}/comments/` - List all comments for a film
- `POST /api/films/{film_id}/comments/` - Add a comment to a film

## Tech Stacks

- Django 4.2
- Django REST Framework
- PostgreSQL (Production) / SQLite (Development)
- drf-spectacular (API Documentation)
- Heroku (Deployment)

## Local Setup
```bash
# Clone repository
git clone <your-repo-url>
cd starwars-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# create superuser
python manage.py createsuperuser

# Sync films from SWAPI
python manage.py shell
>>> from films.swapi_service import SWAPIService
>>> SWAPIService().sync_films()

# Run server..
python manage.py runserver
```

# API Documentation

Visit `/api/docs/` for interactive swagger DOcumentation

## Deployment

Deployed on Heroku with continuous deployment from github

# Author 

Wale Johnson