# task-manager

A simple **Task Management REST API** built with **Django REST Framework**.  

---

## Features

- JWT Authentication
- User-based access control
- CRUD operations for tasks
- Simple filtering

---

## Tech Stack

| Component                       | Description                   |
| ------------------------------- | ----------------------------- |
| **Django**                      | Web framework                 |
| **Django REST Framework (DRF)** | API layer                     |
| **SimpleJWT**                   | JSON Web Token authentication |
| **django-filter**               | Query filtering               |
| **drf-spectacular**             | OpenAPI documentation         |
| **SQLite**                      | Default lightweight database  |
| **DRF `APITestCase`**           | Testing                       |

---

## API Documentation
[Swagger Editor](https://editor.swagger.io/?url=https://raw.githubusercontent.com/salvatoremosca/task-manager/main/schema.yml)

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/salvatoremosca/task-manager.git
cd task-manager-api
```

### 2. Create a virtual environment
```bash
pipenv install
pipenv shell
```

### 3. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser
```bash
python manage.py createsuperuser
```

### 5. Run the server
```bash
python manage.py runserver
```

The API will be available at: http://localhost:8000/api/

Admin panel: http://localhost:8000/admin/

___

## Authentication

The API uses **JWT tokens** for authentication.

### Obtain a Token
```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Include the Token in the requests
```http
Authorization: Bearer <ACCESS_TOKEN>
```

---

## Future Improvements

- Add pagination
- Implement task categories and priorities
- Add user registration endpoint
- Increase test coverage


