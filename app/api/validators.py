from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models import User
from app.models.meeting_room import MeetingRoomModel
from app.models.reservation import ReservationModel


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> MeetingRoomModel:
    meeting_room = await meeting_room_crud.get(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room


async def check_reservation_before_edit(
        reservation_id: int,
        user: User,
        session: AsyncSession,
) -> ReservationModel:
    reservation: ReservationModel = await reservation_crud.get(
        reservation_id, session
    )
    if not reservation:
        raise HTTPException(
            status_code=404,
            detail='Бронь не найдена!'
        )
    if not user.is_superuser or reservation.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужую бронь!'
        )

    return reservation


async def check_reservation_intersections(**kwargs) -> None:
    reservations = (
        await reservation_crud.get_reservations_at_the_same_time(**kwargs)
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations)
        )
