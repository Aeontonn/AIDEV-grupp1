import abc
import json
import os
from pathlib import Path


# Sökväg till filen där användardata lagras (fixad version)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_FILE = os.path.join(DATA_DIR, "users.json")

# Se till att mappen finns
os.makedirs(DATA_DIR, exist_ok=True)

# Om filen inte finns, skapa en tom JSON-lista
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


class BasePlayer(abc.ABC):
    def __init__(self, name: str):
        self.name = name
        self.attempts = 0
        self.time = 0

    @abc.abstractmethod
    def guess(self, lower: int, upper: int) -> int:
        pass


class HumanPlayer(BasePlayer):
    def guess(self, lower: int, upper: int) -> int:
        while True:
            try:
                value = int(input(f"{self.name}, gissa ett tal mellan {lower} och {upper}: "))
                if lower <= value <= upper:
                    self.attempts += 1
                    return value
                else:
                    print("Utanför intervallet!")
            except ValueError:
                print("Ogiltigt input, skriv en siffra!")


def load_users():
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def register_user():
    users = load_users()

    while True:
        username = input("Välj ett användarnamn: ").strip()

        if len(username) < 3:
            print("Användarnamnet måste ha minst 3 tecken.")
            continue
        if not username.isalnum():
            print("Endast bokstäver och siffror är tillåtna.")
            continue
        if any(u["name"] == username for u in users):
            print("Namnet är redan upptaget.")
            continue

        users.append({"name": username, "attempts": 0, "time": 0})
        save_users(users)
        print(f"Användare '{username}' skapad.")
        return HumanPlayer(username)


if __name__ == "__main__":
    player = register_user()
    print(f"Hej {player.name}, nu kan du börja spela.")
