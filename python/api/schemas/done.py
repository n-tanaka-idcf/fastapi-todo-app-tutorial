from pydantic import BaseModel


class DoneResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True
