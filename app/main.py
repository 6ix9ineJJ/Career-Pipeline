from fastapi import FastAPI

from app.database import Base, engine
from app.routers import applications, auth

# Create database tables when the app starts.
# For larger projects, this is usually replaced with migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career Pipeline API",
    description="A FastAPI CRUD project for tracking job applications.",
    version="1.0.0",
)

# Register route groups with the main FastAPI app.
app.include_router(auth.router)
app.include_router(applications.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Career Pipeline API"}
