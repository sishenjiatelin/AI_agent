import csv
import json
from pathlib import Path




def load_text(path: str | Path) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise IsADirectoryError(f"Path is not a file: {file_path}")
    with file_path.open("r",encoding="utf-8") as f:
        text =f.read()
    return text


def save_json(data: object, path: str | Path) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    



def load_csv(path: str | Path) -> list[dict[str, str]]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with file_path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
    
