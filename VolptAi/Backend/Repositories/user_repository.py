from sqlalchemy.orm import Session

from Models.user import User


def get_user_by_username(
        db: Session,
        username: str
):

    return (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )


def create_user(
        db: Session,
        user: User
):

    db.add(user)

    db.commit()

    db.refresh(user)

    return user
def get_user_by_id(
        db,
        user_id
):

    return (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )
