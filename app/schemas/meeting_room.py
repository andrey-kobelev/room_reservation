from typing import Optional

from pydantic import BaseModel, Field, validator


# Базовый класс схемы, от которого наследуем все остальные.
class MeetingRoomBaseSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


# Теперь наследуем схему не от BaseModel, а от MeetingRoomBase.
class MeetingRoomCreateSchema(MeetingRoomBaseSchema):
    # Переопределяем атрибут name, делаем его обязательным.
    name: str = Field(..., min_length=1, max_length=100)
    # Описывать поле description не нужно: оно уже есть в базовом классе.


class MeetingRoomUpdateSchema(MeetingRoomBaseSchema):

    @validator('name')
    def name_cant_be_numeric(cls, name: str):
        if name is None:
            raise ValueError('Поле name не может быть пустым!')
        return name


# Возвращаемую схему унаследуем от MeetingRoomCreate,
# чтобы снова не описывать обязательное поле name.
class MeetingRoomDBSchema(MeetingRoomCreateSchema):
    id: int

    class Config:
        orm_mode = True
