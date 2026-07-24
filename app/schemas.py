from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ApplicationStatus = Literal[
    "Saved",
    "Applied",
    "Screening",
    "Interview",
    "Technical Round",
    "Offer",
    "Rejected",
    "Accepted",
]


class UserCreate(BaseModel):
    # Data required when a new user registers.
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)


class UserRead(BaseModel):
    # from_attributes lets Pydantic convert SQLAlchemy objects into response JSON.
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class Token(BaseModel):
    # Response returned after successful login.
    access_token: str
    token_type: str


class JobApplicationBase(BaseModel):
    # Common fields shared by create and read schemas.
    company_name: str = Field(min_length=1, max_length=100)
    job_title: str = Field(min_length=1, max_length=100)
    status: ApplicationStatus = "Applied"
    location: str | None = Field(default=None, max_length=100)
    salary_range: str | None = Field(default=None, max_length=50)
    applied_date: date | None = None
    notes: str | None = None


class JobApplicationCreate(JobApplicationBase):
    # Request body for creating a new job application.
    pass


class JobApplicationUpdate(BaseModel):
    # All update fields are optional so users can edit only one field at a time.
    company_name: str | None = Field(default=None, min_length=1, max_length=100)
    job_title: str | None = Field(default=None, min_length=1, max_length=100)
    status: ApplicationStatus | None = None
    location: str | None = Field(default=None, max_length=100)
    salary_range: str | None = Field(default=None, max_length=50)
    applied_date: date | None = None
    notes: str | None = None


class JobApplicationRead(JobApplicationBase):
    # Response schema returned from the API.
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    owner_id: int
