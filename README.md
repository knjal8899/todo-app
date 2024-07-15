
# Django Todo App

A simple Todo list application built with Django.

## Features

- User registration and login
- CRUD operations for todo tasks
- JWT token authentication

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:your-username/todo-app.git
cd todo-app

2. Set Up a Virtual Environment
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Create a .env File
Create a .env file (ref. .env-sample) in the root directory and add as mentioned

5. Run Migrations
python manage.py migrate

6. Create a Superuser
python manage.py createsuperuser

7. Start the Development Server
python manage.py runserver
