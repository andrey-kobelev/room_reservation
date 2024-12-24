from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.reservation import (
    ReservationCreateSchema,
    ReservationDBSchema,
    ReservationUpdateSchema
)
from app.crud.reservation import reservation_crud
from app.core.db import get_async_session
from app.api.validators import (
    check_meeting_room_exists,
    check_reservation_intersections,
    check_reservation_before_edit
)
from app.core.user import current_user, current_superuser
from app.models.user import User


router = APIRouter()


@router.post(
    '/',
    response_model=ReservationDBSchema,
)
async def create_reservation(
        reservation: ReservationCreateSchema,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    data = reservation.dict()
    data['session'] = session
    await check_reservation_intersections(**data)
    reservation_db = await reservation_crud.create(reservation, session, user)
    return reservation_db


@router.get(
    '/',
    response_model=list[ReservationDBSchema],
    dependencies=[Depends(current_superuser)],
)
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    reservations_db = await reservation_crud.get_multi(session)
    return reservations_db


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDBSchema
)
async def delete_reservation(
        reservation_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(
        reservation_id, user, session
    )
    reservation = await reservation_crud.remove(reservation, session)
    return reservation


@router.patch('/{reservation_id}', response_model=ReservationDBSchema)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdateSchema,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    reservation = await check_reservation_before_edit(
        reservation_id, user, session
    )
    await check_reservation_intersections(
        **obj_in.dict(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        obj_in=obj_in,
        session=session,
    )
    return reservation


@router.get(
    '/my_reservations',
    response_model=list[ReservationDBSchema]
)
async def get_my_reservations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    reserves = await reservation_crud.get_by_user(user.id, session)
    return reserves
