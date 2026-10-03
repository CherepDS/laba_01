import json
import tomllib
from pathlib import Path
from datetime import datetime
from .errors import DifferentUnits, InvalidUnit
import tomli_w

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = BASE_DIR / "pyproject.toml"
HISTORY_PATH = BASE_DIR / "calc_history.json"

def ensure_config():
    if not CONFIG_PATH.exists():
        default_config = {'length': {'mm': "0.001", 'cm': "0.01", 'm': "1", 'km': "1000"}, 'mass': {'g': "0.001", 'kg': "1"}, 'temperature': {'c': ["273.15", "1"], 'f': ["459.67", "0.5555555555555556"], 'k': ["0", "1"]}}

        with CONFIG_PATH.open("wb") as f:
            tomli_w.dump(default_config, f)

def ensure_history():
    if not HISTORY_PATH.exists():
        with HISTORY_PATH.open("w") as f:
            json.dump([], f)


def get_config():
    ensure_config()
    with open(CONFIG_PATH, "rb") as c:
        data = tomllib.load(c)
    return data

def get_section(unit_1, unit_2):
    data = get_config()
    sec_1 = [i for i in data if unit_1 in data[i]]
    sec_2 = [i for i in data if unit_2 in data[i]]
    if sec_1 and sec_2:
        if sec_1[0] == sec_2[0]:
            return sec_1[0]
        else:
            raise DifferentUnits()
    else:
        raise InvalidUnit()

def save_calc(expr, result):
    ensure_history()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "expression": expr,
        "result": result
    }

    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        history = json.load(f)
        history.append(entry)

    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
