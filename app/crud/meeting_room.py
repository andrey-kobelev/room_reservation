from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoomModel
from .base import CRUDBase


# Создаем новый класс, унаследованный от CRUDBase.
class CRUDMeetingRoom(CRUDBase):

    # Преобразуем функцию в метод класса.
    async def get_room_id_by_name(
            # Дописываем параметр self.
            # В качестве альтернативы здесь можно
            # применить декоратор @staticmethod.
            self,
            room_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await session.execute(
            select(self.model.id).where(
                self.model.name == room_name
            )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id


# Объект crud наследуем уже не от CRUDBase,
# а от только что созданного класса CRUDMeetingRoom.
# Для инициализации передаем модель, как и в CRUDBase.
meeting_room_crud = CRUDMeetingRoom(MeetingRoomModel)


# # Функция работает с асинхронной сессией,
# # поэтому ставим ключевое слово async.
# # В функцию передаём схему MeetingRoomCreate.
# async def create_meeting_room(
#         new_room: MeetingRoomCreateSchema,
#         session: AsyncSession,
# ) -> MeetingRoomModel:
#     # Конвертируем объект MeetingRoomCreate в словарь.
#     new_room_data = new_room.dict()
#
#     # Создаём объект модели MeetingRoom.
#     # В параметры передаём пары "ключ=значение", для этого распаковываем словарь.
#     db_room = MeetingRoomModel(**new_room_data)
#
#     # Добавляем созданный объект в сессию.
#     # Никакие действия с базой пока ещё не выполняются.
#     session.add(db_room)
#
#     # Записываем изменения непосредственно в БД.
#     # Так как сессия асинхронная, используем ключевое слово await.
#     await session.commit()
#
#     # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
#     await session.refresh(db_room)
#     # Возвращаем только что созданный объект класса MeetingRoom.
#     return db_room

# async def read_all_rooms_from_db(session: AsyncSession) -> list[MeetingRoomModel]:
#     rooms = await session.execute(
#         select(MeetingRoomModel)
#     )
#     rooms = rooms.scalars().all()
#     return rooms
#
#
# async def get_meeting_room_by_id(room_id: int, session: AsyncSession) -> Optional[MeetingRoomModel]:
#     db_room = await session.execute(
#         select(MeetingRoomModel).where(
#             MeetingRoomModel.id == room_id
#         )
#     )
#     db_room = db_room.scalars().first()
#     return db_room
#
#
# async def update_meeting_room(
#         # Объект из БД для обновления.
#         db_room: MeetingRoomModel,
#         # Объект из запроса.
#         room_in: MeetingRoomUpdateSchema,
#         session: AsyncSession,
# ) -> MeetingRoomModel:
#     # Представляем объект из БД в виде словаря.
#     obj_data = jsonable_encoder(db_room)
#     # Конвертируем объект с данными из запроса в словарь,
#     # исключаем неустановленные пользователем поля.
#     update_data = room_in.dict(exclude_unset=True)
#
#     # Перебираем все ключи словаря, сформированного из БД-объекта.
#     for field in obj_data:
#         # Если конкретное поле есть в словаре с данными из запроса, то...
#         if field in update_data:
#             # ...устанавливаем объекту БД новое значение атрибута.
#             setattr(db_room, field, update_data[field])
#     # Добавляем обновленный объект в сессию.
#     session.add(db_room)
#     # Фиксируем изменения.
#     await session.commit()
#     # Обновляем объект из БД.
#     await session.refresh(db_room)
#     return db_room
#
#
# async def delete_meeting_room(
#         db_room: MeetingRoomModel,
#         session: AsyncSession,
# ) -> MeetingRoomModel:
#     # Удаляем объект из БД.
#     await session.delete(db_room)
#     # Фиксируем изменения в БД.
#     await session.commit()
#     # Не обновляем объект через метод refresh(),
#     # следовательно он всё ещё содержит информацию об удаляемом объекте.
#     return db_room