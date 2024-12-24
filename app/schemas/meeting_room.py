from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBaseSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreateSchema(MeetingRoomBaseSchema):
    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomUpdateSchema(MeetingRoomBaseSchema):

    @validator('name')
    def name_cant_be_numeric(cls, name: str):
        if name is None:
            raise ValueError('Поле name не может быть пустым!')
        return name


class MeetingRoomDBSchema(MeetingRoomCreateSchema):
    id: int

    class Config:
        orm_mode = True
