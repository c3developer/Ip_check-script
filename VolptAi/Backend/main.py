from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from dependencies import get_db

from Schemas.user_schema import UserCreate
from Schemas.auth_schema import LoginRequest

from Services.auth_service import (
    register_user,
    login_user
)
from Schemas.chat_schema import (
    CreateSessionRequest,
    ChatRequest
)

from Services.chat_service import (
    create_chat_session
)
from Services.ollama_service import ask_ai

from Services.chat_service import (
    create_chat_session,
    save_user_message,
    save_ai_message
)
from Repositories.session_repository import (
    get_user_sessions
)

from Repositories.message_repository import (
    get_messages_by_session
)
from auth_dependency import (
    get_current_username
)

from Repositories.user_repository import (
    get_user_by_username
)
from fastapi import HTTPException
from Repositories.session_repository import (
    get_session
)
from Models.user_settings import UserSettings

from Schemas.settings_schema import (
    SettingsRequest
)

from Repositories.settings_repository import (
    get_user_settings,
    create_settings,
    update_settings
)
from Repositories.session_repository import (
    get_session,
    delete_session,
    rename_session
)

app = FastAPI(
    title="VOLPT AI API",
    version="1.0"
)


@app.get("/")
def root():

    return {
        "message": "VOLPT AI Backend"
    }


@app.post("/register")
def register(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    try:

        created_user = register_user(
            db,
            user.username,
            user.email,
            user.password
        )

        return {
            "message": "User created",
            "id": created_user.id
        }

    except Exception as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )


@app.post("/login")
def login(
        request: LoginRequest,
        db: Session = Depends(get_db)
):

    token = login_user(
        db,
        request.username,
        request.password
    )

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/chat/create")
def create_chat(

        request: CreateSessionRequest,

        username: str = Depends(
            get_current_username
        ),

        db: Session = Depends(get_db)

):

    user = get_user_by_username(
        db,
        username
    )

    session = create_chat_session(

        db,

        user.id,

        request.title
    )

    return {

        "session_id": session.id,

        "title": session.title
    }
@app.post("/chat/send")
def send_message(
        request: ChatRequest,
        db: Session = Depends(get_db)
):

    save_user_message(
        db,
        request.session_id,
        request.message
    )

    ai_response = ask_ai(
        request.message
    )

    save_ai_message(
        db,
        request.session_id,
        ai_response
    )

    return {
        "response": ai_response
    }
@app.get("/chat/list")
def chat_list(

        username: str = Depends(
            get_current_username
        ),

        db: Session = Depends(get_db)

):

    user = get_user_by_username(
        db,
        username
    )

    sessions = get_user_sessions(
        db,
        user.id
    )

    return [

        {
            "id": s.id,
            "title": s.title
        }

        for s in sessions
    ]
@app.get("/chat/history/{session_id}")
def chat_history(

        session_id: int,

        username: str = Depends(
            get_current_username
        ),

        db: Session = Depends(get_db)

):

    user = get_user_by_username(
        db,
        username
    )

    session = get_session(
        db,
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    if session.user_id != user.id:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    messages = get_messages_by_session(
        db,
        session_id
    )

    return [

        {
            "role": m.role,
            "content": m.content
        }

        for m in messages
    ]
@app.get("/settings")
def get_settings(

        username: str = Depends(
            get_current_username
        ),

        db: Session = Depends(get_db)

):

    user = get_user_by_username(
        db,
        username
    )

    settings = get_user_settings(
        db,
        user.id
    )

    if not settings:

        settings = UserSettings(

            user_id=user.id,

            theme="dark",

            font_size=12,

            ai_model="phi3:mini",

            system_prompt=""
        )

        create_settings(
            db,
            settings
        )

    return {

        "theme": settings.theme,

        "font_size": settings.font_size,

        "ai_model": settings.ai_model,

        "system_prompt": settings.system_prompt
    }
@app.post("/settings")
def save_settings(

        request: SettingsRequest,

        username: str = Depends(
            get_current_username
        ),

        db: Session = Depends(get_db)

):

    user = get_user_by_username(
        db,
        username
    )

    settings = get_user_settings(
        db,
        user.id
    )

    if not settings:

        settings = UserSettings(
            user_id=user.id
        )

        create_settings(
            db,
            settings
        )

    settings.theme = request.theme

    settings.font_size = request.font_size

    settings.ai_model = request.ai_model

    settings.system_prompt = request.system_prompt

    update_settings(
        db,
        settings
    )

    return {
        "message": "saved"
    }
@app.delete("/chat/delete/{session_id}")
def delete_chat(

        session_id: int,

        username: str = Depends(
            get_current_username
        ),

        db: Session = Depends(get_db)

):

    user = get_user_by_username(
        db,
        username
    )

    session = get_session(
        db,
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    if session.user_id != user.id:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    delete_session(
        db,
        session_id
    )

    return {
        "message": "deleted"
    }
@app.put("/chat/rename/{session_id}")
def rename_chat(

        session_id: int,

        title: str,

        username: str = Depends(
            get_current_username
        ),

        db: Session = Depends(get_db)

):

    user = get_user_by_username(
        db,
        username
    )

    session = get_session(
        db,
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    if session.user_id != user.id:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    rename_session(
        db,
        session_id,
        title
    )

    return {
        "message": "renamed"
    }