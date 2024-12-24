from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, validator, root_validator, Extra, Field


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBaseSchema(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


class ReservationUpdateSchema(ReservationBaseSchema):

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, from_reserve: datetime):
        if from_reserve >= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return from_reserve

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, data):
        if data['from_reserve'] >= data['to_reserve']:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return data


class ReservationCreateSchema(ReservationBaseSchema):
    meetingroom_id: int


class ReservationDBSchema(ReservationBaseSchema):
    id: int
    meetingroom_id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True
