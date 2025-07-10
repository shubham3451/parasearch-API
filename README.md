# Paragraph searching API

A Django REST API to store multiple paragraphs and search for paragraphs containing specific words.

---

## Features

* User registration and JWT authentication.
* Store multiple paragraphs per user.
* Tokenize and index words against paragraphs (case-insensitive).
* Search API returns top 10 paragraphs containing a given word.
* PostgreSQL for persistent storage.
* Swagger UI API documentation via `drf-spectacular`.
* Fully Dockerized setup for easy local development and deployment.

---

## Tech Stack

* Python 3.11, Django 4.x
* Django REST Framework (DRF)
* PostgreSQL
* Docker & Docker Compose
* JWT Authentication (`djangorestframework-simplejwt`)
* API documentation with `drf-spectacular`

---

## Getting Started

### Prerequisites

* Docker and Docker Compose installed locally
* Git

---

### Setup and Run (Docker)

1. Clone the repository:

```bash
git clone <repo-url>
cd <project-folder>
```

2. Create a `.env` file in the root directory with the following content:

```env
DEBUG=1
SECRET_KEY=your_secret_key_here

DB_NAME=myprojectdb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432

POSTGRES_DB=myprojectdb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
```

3. Build and start the containers:

```bash
docker-compose up --build
```

4. Create a superuser to access Django admin:

```bash
docker-compose exec web python manage.py createsuperuser
```

5. Visit:

* API docs: [http://localhost:8000/api/docs/swagger](http://127.0.0.1:8000/api/docs/swagger/)
* Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

### Local Development (Without Docker)

1. Ensure PostgreSQL is installed and running locally.
2. Create a DB and user (see PostgreSQL setup instructions).
3. Clone repo and create a virtual environment:

```bash
git clone <repo-url>
cd <project-folder>
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

4. Configure database in `settings.py`.
5. Run migrations and start server:

```bash
python manage.py migrate
python manage.py runserver
```

---

## API Usage

### Authentication

* Register: `POST /api/auth/register/`
* Login: `POST /api/auth/login/` (returns JWT tokens)
* Use JWT access token in `Authorization: Bearer <token>` header for protected endpoints.

### Endpoints

* `POST /api/paragraphs/` — Submit paragraphs text (multiple paragraphs separated by two newlines).
* `GET /api/search/?word=<word>` — Search top 10 paragraphs containing the word.

---

### Example Payload to Create Paragraphs

```json
{
   Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor...
      
   Maecenas volutpat blandit aliquam etiam erat velit scelerisque...
    
}
```

---

### Example Search

Request:

```http
GET /api/search/?word=lorem
Authorization: Bearer <your_access_token>
```

Response:

```json
[
  {
    "id": "uuid-of-paragraph",
    "content": "Paragraph text containing lorem...",
    "created_by": "user-id",
    "created_at": "2025-07-10T12:34:56Z"
  }
]
```

---

## Swagger/OpenAPI Documentation

* Visit [http://localhost:8000/api/docs/swagger](http://127.0.0.1:8000/api/docs/swagger/) for interactive API docs.



## Project Structure

```
prject/
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── utils.py
│   └── permissions.py
├── users/
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── managers.py
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── README.md

```

---

## License

MIT License

---
