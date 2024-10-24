import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    APP_NAME: str = os.getenv("APP_NAME", "localhost") + "_api"
    APP_VERSION: str = "1.0.0"
    APP_DEBUG: bool = os.getenv("APP_DEBUG", True)
    APP_ENV: str = os.getenv("APP_ENV", "development")
    PORT: str = os.getenv("APP_PORT", "8001")

config = Config()
