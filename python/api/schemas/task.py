from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: str | None = Field(default=None, examples=["クリーニングを取りに行く"])
    done: bool = Field(default=False, description="完了フラグ")
