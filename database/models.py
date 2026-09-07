# Only define tables: YouTube, Meeting and Task

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, UTC
from database.database import engine

Base = declarative_base()


# ==============================
# YOUTUBE MODEL
# ==============================
class YouTube(Base):
    __tablename__ = "youtube"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    transcript = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))


# ==============================
# MEETING MODEL
# ==============================
class Meeting(Base):
    __tablename__ = "meeting"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    transcript = Column(Text)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    tasks = relationship(
        "Task", back_populates="meeting"
    )  # This Meeting class is related to the Task class.


# ==============================
# TASK MODEL
# ==============================
class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meeting.id"))
    task = Column(Text, nullable=False)
    owner = Column(String)
    status = Column(String, default="Pending")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    meeting = relationship("Meeting", back_populates="tasks")


# ==============================
# Telling SQLAlchemy to create the tables.
# ==============================
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
