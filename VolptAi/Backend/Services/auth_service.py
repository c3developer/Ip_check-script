from Models.user import User

from security import (
    hash_password,
    verify_password,
    create_access_token
)

from Repositories.user_repository import (
    get_user_by_username,
    create_user
)


def register_user(
        db,
        username,
        email,
        password
):

    existing = get_user_by_username(
        db,
        username
    )

    if existing:

        raise Exception(
            "User already exists"
        )

    user = User(

        username=username,

        email=email,

        password_hash=hash_password(
            password
        )
    )

    return create_user(
        db,
        user
    )


def login_user(
        db,
        username,
        password
):

    user = get_user_by_username(
        db,
        username
    )

    if not user:

        return None

    if not verify_password(
            password,
            user.password_hash
    ):

        return None

    token = create_access_token(
        {
            "sub": username
        }
    )

    return token