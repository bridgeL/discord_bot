import inspect
from pathlib import Path
from typing import List
from ._bot import bot as _bot


class App:
    bot = _bot

    def __init__(self, name: str, help="开发者太懒了，没有写帮助") -> None:
        path = Path(inspect.stack()[1].filename).resolve(
        ).relative_to(Path("plugins").resolve())

        parts = list(path.with_suffix("").parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]

        if len(parts) > 1:
            parts[-1] = name
            name = ".".join(parts)

        self.name = name
        self.state_dict = {}
        self.help = help

        ALL_APPS.append(self)

    @property
    def state(self):
        # id = f"{self.bot.cid}_{self.bot.uid}"
        id = self.bot.cid
        return self.state_dict.get(id, "")

    @state.setter
    def state(self, v):
        # id = f"{self.bot.cid}_{self.bot.uid}"
        id = self.bot.cid
        self.state_dict[id] = v

    def wrap_check_state(self, func, state):
        async def _func(*args, **kwargs):
            if self.state != state:
                return
            await func(*args, **kwargs)
        return _func

    # on_xxx decorator

    def on_cmd(self, cmd: str, state=""):
        def decorator(func):
            func = self.wrap_check_state(func, state)
            self.bot.cmd_hook_point.add(cmd, func)
            return func
        return decorator

    def on_regex(self, cmd: str, state=""):
        def decorator(func):
            func = self.wrap_check_state(func, state)
            self.bot.cmd_hook_point.add(cmd, func, True)
            return func
        return decorator

    # important function

    async def send(self, text: str, cid=0):
        await self.bot.send(text, cid)

    async def send_help(self, cid=0):
        await self.bot.send(f"=== {self.name} 使用帮助 ===\n\n"+self.help, cid)


ALL_APPS: List[App] = []
