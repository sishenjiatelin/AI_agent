from datetime import datetime
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[0]
LOG_FILE = BASE_DIR / "logs" /"day01.log"
ENV_FILE = BASE_DIR / ".env"

def load_app_name(path:Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("APP_NAME"):
            return line.split("=",1)[1].strip()



def main() -> None:
    app_name = load_app_name(ENV_FILE)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with LOG_FILE.open("w",encoding="utf-8") as f:
        f.write(f"{app_name} started successfully at {now}\n")


    print(f"{app_name} started at {now}")


if __name__ == "__main__":
    main()
