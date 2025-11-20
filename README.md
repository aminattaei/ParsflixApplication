# Parsflix Application

A Django-based web application for managing and displaying movies.

## Description

Parsflix Application is a web platform built using Django framework that allows users to browse and manage movie collections. The application includes a Movie app for handling movie-related functionalities.

## Features

- Django admin interface for content management
- Static and media file handling
- Template-based rendering
- Modular app structure with Movie app

## Installation

1. Ensure you have Python installed on your system.
2. Install Django:
   ```
   pip install django
   ```
3. Clone or download the project files.
4. Navigate to the project directory.
5. Run the development server:
   ```
   python manage.py runserver
   ```
6. Open your browser and go to `http://127.0.0.1:8000/` to access the application.

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin/` for administrative tasks.
- The application is currently in development phase with basic Django setup.

## Deployment

For production deployment:

1. Install production dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Collect static files:
   ```
   python manage.py collectstatic --noinput
   ```

3. Run with Gunicorn:
   ```
   gunicorn core.wsgi:application --bind 0.0.0.0:8000
   ```

4. For better production setup, use a reverse proxy like Nginx.

## Technologies Used

- Django 5.2.8
- Gunicorn (for production server)
- PostgreSQL (database)
- Python

## Contributing

Contributions are welcome. Please follow standard Django development practices.

## License

This project is licensed under the MIT License.