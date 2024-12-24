from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.crud.base import CRUDBase
from app.models.reservation import ReservationModel


class CRUDReservation(CRUDBase):

    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> list[ReservationModel]:
        select_stmt = select(self.model).where(
            self.model.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= self.model.to_reserve,
                to_reserve >= self.model.from_reserve
            )
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                self.model.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession
    ):
        reservations = await session.execute(
            select(self.model).where(
                self.model.meetingroom_id == room_id,
                self.model.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_by_user(self, user_id: int, session: AsyncSession):
        user_reserves = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        user_reserves = user_reserves.scalars().all()
        return user_reserves

    async def get_count_res_at_the_same_time(
            self,
            from_reserve: datetime,
            to_reserve: datetime,
            session: AsyncSession,
    ) -> list[dict[str, int]]:
        reservations = await session.execute(
            select(
                self.model.meetingroom_id,
                func.count(self.model.meetingroom_id)
            ).where(
                self.model.from_reserve >= from_reserve,
                self.model.to_reserve <= to_reserve
            ).group_by(self.model.meetingroom_id)
        )
        reservations = reservations.all()
        return reservations


reservation_crud = CRUDReservation(ReservationModel)
