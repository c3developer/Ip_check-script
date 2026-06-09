from Models.session import Session
from Models.message import Message

def create_session(
        db,
        session
):

    db.add(session)

    db.commit()

    db.refresh(session)

    return session


def get_session(
        db,
        session_id
):

    return (
        db.query(Session)
        .filter(
            Session.id == session_id
        )
        .first()
    )
def get_all_sessions(db):

    return (
        db.query(Session)
        .order_by(Session.id.desc())
        .all()
    )
def get_user_sessions(
        db,
        user_id
):

    return (

        db.query(Session)

        .filter(
            Session.user_id == user_id
        )

        .order_by(
            Session.id.desc()
        )

        .all()
    )
def get_session(
        db,
        session_id
):

    return (

        db.query(Session)

        .filter(
            Session.id == session_id
        )

        .first()
    )

def delete_session(
        db,
        session_id
):

    db.query(Message).filter(
        Message.session_id == session_id
    ).delete()

    session = get_session(
        db,
        session_id
    )

    if session:

        db.delete(session)

        db.commit()


def rename_session(
        db,
        session_id,
        new_title
):

    session = get_session(
        db,
        session_id
    )

    if session:

        session.title = new_title

        db.commit()

        db.refresh(session)

    return session