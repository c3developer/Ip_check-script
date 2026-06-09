from sqlalchemy import *

from Models.user import Base


class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True
    )

    session_id = Column(
        Integer,
        ForeignKey("sessions.id")
    )

    role = Column(
        String(20)
    )

    content = Column(
        Text
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )