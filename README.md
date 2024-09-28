Django REST API with CRUD Operations

Prerequisites
Make sure you have the following installed:
Python 3.x,
pip,
MySQL

Step 1: Create a Virtual Environment: virtualenv env
Activate the virtual environment: env\Scripts\activate

Step 2: Install Required Libraries
pip install django==4.1 djangorestframework,mysqlclient,django-redis,
pip install djangorestframework-simplejwt.
pip install loguru
pip install pytest pytest-django
crearatte model class and serialer class.
py manage.py makemigrations
py manage.py migrate

For Signup-
http://127.0.0.1:8000/api/signup/

{
    "username": "your_username",
    "password": "your_password",
    "email": "your_email@example.com"
}


Response:
{
    "username": "your_username",
    "email": "your_email@example.com",
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}

Get Access and Refresh Tokens:
http://127.0.0.1:8000/api/token/


CRUD Operations
BASE URL-http://127.0.0.1:8000/

List All Items
URL: GET /api/items/

Create a New Item
URL: POST /api/items/

Retrieve a Single Item
/api/items/{id}/

Update an Item
/api/items/{id}/

Partially Update an Item
URL: PATCH /api/items/{id}/

Delete an Item
URL: DELETE /api/items/{id}/

Get Popular Items
api/items/popular/

Requirements
To install all dependencies, run:
pip freeze >requirements.txt
