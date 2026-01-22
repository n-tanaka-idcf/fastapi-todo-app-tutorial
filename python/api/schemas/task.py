import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str | None = Field(default=None, examples=["クリーニングを取りに行く"])
    due_date: datetime.date | None = Field(default=None, examples=["2024-12-01"])


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True


class Task(TaskBase):
    id: int
    done: bool = Field(default=False, description="完了フラグ")

    class Config:
        from_attributes = True
