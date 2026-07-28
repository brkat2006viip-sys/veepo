import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/bot.db")
    FERNET_KEY: str = os.getenv("FERNET_KEY", "")
    AGENTROUTER_API_URL: str = os.getenv("AGENTROUTER_API_URL", "https://api.agentrouter.example")
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "")
    WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", 8443))

settings = Settings()
