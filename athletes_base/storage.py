import os
import json

BASE_PATH = "./database/ajbase.json"

def is_exist() -> bool:
    return os.path.exists(BASE_PATH)


def init_base():
    if not is_exist():
        os.makedirs(os.path.dirname(BASE_PATH), exist_ok=True)

        with open(BASE_PATH, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=4)


def read_base() -> list[dict]:
    init_base()

    with open(BASE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


def write_base(data: list[dict]):
    init_base()

    with open(BASE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)