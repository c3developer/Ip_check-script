DATABASE_URL = (
    "postgresql+psycopg://postgres:123456@localhost:5432/volpt_ai"
)

SECRET_KEY = "volpt_ai_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 1440

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "phi3:mini"