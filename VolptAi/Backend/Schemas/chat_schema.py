from pydantic import BaseModel

class CreateSessionRequest(BaseModel):

    title: str


class ChatRequest(BaseModel):

    session_id: int

    message: str