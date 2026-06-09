from pydantic import BaseModel


class SettingsRequest(BaseModel):

    theme: str

    font_size: int

    ai_model: str

    system_prompt: str