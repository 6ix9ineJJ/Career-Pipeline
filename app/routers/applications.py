from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import JobApplication, User
from app.schemas import (
    JobApplicationCreate,
    JobApplicationRead,
    JobApplicationUpdate,
)

# APIRouter groups all job application CRUD endpoints in one file.
router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=list[JobApplicationRead])
def list_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[JobApplication]:
    # READ: return only the job applications owned by the logged-in user.
    query = select(JobApplication).where(JobApplication.owner_id == current_user.id)
    return list(db.scalars(query).all())


@router.post(
    "",
    response_model=JobApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application_data: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobApplication:
    # CREATE: convert the validated Pydantic data into a SQLAlchemy model object.
    application = JobApplication(
        **application_data.model_dump(),
        owner_id=current_user.id,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/{application_id}", response_model=JobApplicationRead)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobApplication:
    # READ ONE: search by id and owner_id so users cannot access other users' data.
    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.owner_id == current_user.id,
        )
    )
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put("/{application_id}", response_model=JobApplicationRead)
def update_application(
    application_id: int,
    application_data: JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobApplication:
    # UPDATE: first find the record that belongs to the logged-in user.
    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.owner_id == current_user.id,
        )
    )
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    # exclude_unset=True keeps unchanged fields as they are in the database.
    update_data = application_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    # DELETE: remove one application if it belongs to the logged-in user.
    application = db.scalar(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.owner_id == current_user.id,
        )
    )
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()
