import json
from pathlib import Path
from pydantic import BaseModel


class User(BaseModel):
    uid: int
    checkin_date: str = ""
    money: int = 0
    msg_cnt: int = 0


class Manager:
    def __init__(self) -> None:
        self.path = Path(__file__).with_name("data.json")

        if not self.path.exists():
            with self.path.open("w+", encoding="utf8") as f:
                f.write("[]")

        data = json.loads(self.path.read_text("utf8"))
        self.users = [User(**d) for d in data]

    def get(self, uid: int):
        for user in self.users:
            if user.uid == uid:
                return user
        user = User(uid=uid)
        self.users.append(user)
        self.save()
        return user

    def save(self):
        data = [user.model_dump() for user in self.users]
        self.path.write_text(json.dumps(
            data, ensure_ascii=False, indent=4), "utf8")


manager = Manager()
