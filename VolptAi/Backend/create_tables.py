from database import engine

from Models.user import Base

import Models.user
import Models.user_settings
import Models.session
import Models.message

Base.metadata.create_all(bind=engine)

print("TABLES CREATED")