from sqlalchemy import *

from Models.user import Base


class UserSettings(Base):

    __tablename__ = "user_settings"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    theme = Column(
        String(20),
        default="dark"
    )

    font_size = Column(
        Integer,
        default=12
    )

    ai_model = Column(
        String(100),
        default="phi3:mini"
    )

    system_prompt = Column(
        Text,
        default=""
    )