import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "AI Job Agent")
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", "data"))
    LOG_DIR: Path = Path(os.getenv("LOG_DIR", "logs"))


settings = Settings()