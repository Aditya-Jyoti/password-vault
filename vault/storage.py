import json
from typing import Optional

def read_content() -> dict:
    try:
        with open(r"storage/PasswordVault.txt", "r") as file:
            obj = json.load(file)
            return obj 
    except json.decoder.JSONDecodeError:
        with open(r"storage/PasswordVault.txt", "w") as file:
            obj = json.dumps({}, indent=4)
            file.write(obj)
        return read_content()

def write_content(data: dict) -> Optional[bool]:
    try:
        with open(r"storage/PasswordVault.txt", "w") as file:
            obj = json.dumps(data, indent= 4)
            file.write(obj)
            return True

    except FileNotFoundError:
        return

def clean_file() -> None:
    return open(r"storage/PasswordVault.txt", "w").close()

if __name__ == "__main__":
    clean_file()
