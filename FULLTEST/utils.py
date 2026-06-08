import re
import json
from pathlib import Path

def Load_Text(path: Path | str) -> str:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as f:
        text = f.read()
    return text

def Save_Json(data: any, path: Path | str) -> None:
    file_path = Path(path)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent= 2)



def Extract_LabelContent(path: Path | str, label: str) -> list[str] | str:
    text = Load_Text(path)
    pattern = rf"(?m)^[ \t]*{re.escape(label)}[ \t]*[:：][ \t]*([^\r\n]*)"
    result = re.search(pattern,text).group(1)
    if label == "技能要求" :
        return [skill.strip() for skill in re.split(r"[、,，.。]", result)]
    if label == "经验要求" :
        exp = re.split(r"[年]", result)
        return exp[0]
    return result



