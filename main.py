from datetime import datetime
from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "day01.log"


def main() -> None:
    load_dotenv(BASE_DIR / ".env")

    app_name = os.getenv("APP_NAME", "AI Job Learning Agent")
    app_env = os.getenv("APP_ENV", "dev")

    now = datetime.now().isoformat(timespec="seconds")
    message = f"[{now}] {app_name} is ready. env={app_env}"

    print(message)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(message + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
