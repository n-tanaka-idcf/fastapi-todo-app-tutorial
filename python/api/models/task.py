from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column(String(1024))
    due_date: Mapped[date | None] = mapped_column(Date)

    done: Mapped["Done"] = relationship("Done", back_populates="task", cascade="delete", uselist=False)


class Done(Base):
    __tablename__ = "dones"

    id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)

    task: Mapped["Task"] = relationship("Task", back_populates="done")
