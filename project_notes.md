# Career Pipeline Notes

## Project Stack
- Frontend: Streamlit
- Backend: FastAPI
- Database: SQLite
- ORM: SQLAlchemy
- Auth: JWT token authentication

## GitHub Basics
- Git tracks local code changes.
- GitHub stores repositories online for backup and collaboration.
- Repository: project folder with code and history.
- Commit: saved snapshot of changes.
- Push: send local commits to GitHub.
- Pull: get latest changes from GitHub.
- Clone: download a repo to your computer.
- Branch: separate line of work.
- Pull request: review and merge code changes.

## FastAPI Basics
- FastAPI is a Python framework for building APIs.
- Endpoint: API route like `GET /applications`.
- `GET`: read data.
- `POST`: create data.
- `PUT`: update data.
- `DELETE`: remove data.
- Swagger docs are available at `/docs`.
- Dependencies are used for database sessions and current user auth.

## Pydantic
- Pydantic validates request and response data.
- FastAPI uses Pydantic schemas to check incoming JSON.
- If required fields are missing or wrong, FastAPI returns a validation error.

## JWT Auth
- JWT is a token used to prove the user is logged in.
- Login returns an access token.
- Streamlit stores the token in session state.
- Protected API calls send the token in the `Authorization` header.

## Important Status Codes
- `200 OK`: request successful.
- `201 Created`: new data created.
- `400 Bad Request`: invalid request or duplicate data.
- `401 Unauthorized`: missing or invalid token.
- `403 Forbidden`: logged in but not allowed.
- `404 Not Found`: route or record not found.
- `422 Unprocessable Entity`: Pydantic validation failed.
- `500 Internal Server Error`: backend/server bug.

## Project API Endpoints
- `GET /`
- `POST /auth/register`
- `POST /auth/token`
- `GET /auth/me`
- `GET /applications`
- `POST /applications`
- `GET /applications/{application_id}`
- `PUT /applications/{application_id}`
- `DELETE /applications/{application_id}`

## Short Project Explanation
Career Pipeline is a job application tracker. Users log in with JWT authentication, then manage job applications through a Streamlit dashboard connected to a FastAPI backend and SQLite database using SQLAlchemy.
