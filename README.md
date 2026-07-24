# Career Pipeline

Career Pipeline is a bootcamp-friendly CRUD project for managing job applications.

It covers:

- Python project structure
- FastAPI backend development
- Pydantic request/response validation
- SQLAlchemy database models
- SQLite database storage
- JWT authentication
- CRUD operations
- Streamlit frontend
- GitHub README documentation

## Project Features

- Register a new user
- Log in with username and password
- Add job applications
- View all job applications
- Update application status and notes
- Delete old applications

## Application Status Flow

Example statuses:

- Saved
- Applied
- Screening
- Interview
- Technical Round
- Offer
- Rejected
- Accepted

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirement.txt
```

## Run The FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Open the Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

## Run The Streamlit Frontend

Open a second terminal, activate the same virtual environment, then run:

```bash
streamlit run streamlit_app.py
```

## Main API Endpoints

- `POST /auth/register` - create a user account
- `POST /auth/token` - log in and receive a JWT token
- `GET /applications` - list job applications
- `POST /applications` - create a job application
- `GET /applications/{application_id}` - view one job application
- `PUT /applications/{application_id}` - update a job application
- `DELETE /applications/{application_id}` - delete a job application

## Folder Structure

```text
app/
  main.py
  database.py
  models.py
  schemas.py
  auth.py
  routers/
    auth.py
    applications.py
streamlit_app.py
requirement.txt
README.md
```

## Bootcamp Explanation

FastAPI creates the API routes, Pydantic validates incoming data, SQLAlchemy talks to the SQLite database, JWT protects private routes, and Streamlit provides a simple user interface.
