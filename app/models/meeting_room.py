from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class MeetingRoomModel(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    reservations = relationship('ReservationModel', cascade='delete')
