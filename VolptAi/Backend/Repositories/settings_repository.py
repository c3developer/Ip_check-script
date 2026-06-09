from Models.user_settings import UserSettings


def get_user_settings(
        db,
        user_id
):

    return (

        db.query(UserSettings)

        .filter(
            UserSettings.user_id == user_id
        )

        .first()
    )


def create_settings(
        db,
        settings
):

    db.add(settings)

    db.commit()

    db.refresh(settings)

    return settings


def update_settings(
        db,
        settings
):

    db.commit()

    db.refresh(settings)

    return settings