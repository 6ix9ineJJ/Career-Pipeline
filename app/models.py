from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    # This table stores registered users.
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    # One user can have many job applications.
    applications: Mapped[list["JobApplication"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class JobApplication(Base):
    # This table stores the CRUD records for the Career Pipeline app.
    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String(100), index=True)
    job_title: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(30), default="Applied")
    location: Mapped[str | None] = mapped_column(String(100), default=None)
    salary_range: Mapped[str | None] = mapped_column(String(50), default=None)
    applied_date: Mapped[date | None] = mapped_column(Date, default=None)
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # This connects each application back to the user who created it.
    owner: Mapped[User] = relationship(back_populates="applications")
