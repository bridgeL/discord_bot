from typing import List
from ._bot import bot as _bot


class App:
    bot = _bot

    def __init__(self, name: str, help="开发者太懒了，没有写帮助") -> None:
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
        await self.bot.send(self.help, cid)


ALL_APPS: List[App] = []
