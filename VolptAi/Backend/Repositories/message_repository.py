from Models.message import Message


def create_message(
        db,
        message
):

    db.add(message)

    db.commit()

    db.refresh(message)

    return message


def get_messages_by_session(
        db,
        session_id
):

    return (
        db.query(Message)
        .filter(
            Message.session_id == session_id
        )
        .all()
    )
def get_messages_by_session(
        db,
        session_id
):

    return (
        db.query(Message)
        .filter(
            Message.session_id == session_id
        )
        .order_by(Message.id)
        .all()
    )