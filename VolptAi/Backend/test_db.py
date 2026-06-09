from sqlalchemy import text

from database import engine

try:

    with engine.connect() as connection:

        connection.execute(
            text("SELECT 1")
        )

        print("DATABASE OK")

except Exception as ex:

    print(ex)