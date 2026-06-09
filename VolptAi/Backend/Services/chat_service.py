from Models.session import Session

from Models.message import Message

from Repositories.session_repository import (
    create_session
)

from Repositories.message_repository import (
    create_message
)


def create_chat_session(
        db,
        user_id,
        title
):

    session = Session(

        user_id=user_id,

        title=title
    )

    return create_session(
        db,
        session
    )


def save_user_message(
        db,
        session_id,
        text
):

    message = Message(

        session_id=session_id,

        role="user",

        content=text
    )

    return create_message(
        db,
        message
    )


def save_ai_message(
        db,
        session_id,
        text
):

    message = Message(

        session_id=session_id,

        role="assistant",

        content=text
    )

    return create_message(
        db,
        message
    )