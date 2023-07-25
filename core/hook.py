import re
import typing
import asyncio
from .constant import PREFIXES
from .context import CURRENT_CMD, CURRENT_PREFIX, CURRENT_TEXT, CURRENT_REGEX


async def do_nothing(): pass


class Hook:
    def __init__(self, func=do_nothing) -> None:
        self.func = func

    async def check(self, *args, **kwargs):
        return True

    async def run(self, *args, **kwargs):
        if await self.check(*args, **kwargs):
            await self.func()


KT = typing.TypeVar("KT", bound=Hook)


class HookPoint(typing.Generic[KT]):
    def __init__(self) -> None:
        self.hooks: typing.List[KT] = []

    async def run(self, *args, **kwargs):
        for hook in self.hooks:
            asyncio.create_task(hook.run(*args, **kwargs))


class CmdFullMatchHook(Hook):
    def __init__(self, cmd: str, func) -> None:
        self.cmd = cmd
        self.func = func

    async def check(self, text: str):
        for p in PREFIXES:
            if text.startswith(p+self.cmd):
                CURRENT_PREFIX.set(p)
                CURRENT_CMD.set(self.cmd)
                CURRENT_TEXT.set(text[len(p+self.cmd):].strip())
                return True
        return False


class CmdRegexMatchHook(Hook):
    def __init__(self, cmd: str, func) -> None:
        self.cmd = cmd
        self.func = func
        self.patt = re.compile(cmd)

    async def check(self, text: str):
        for p in PREFIXES:
            if text.startswith(p):
                r = self.patt.search(text[len(p):])
                if r:
                    CURRENT_PREFIX.set(p)
                    CURRENT_CMD.set(self.cmd)
                    CURRENT_TEXT.set(text[len(p):][r.span()[1]:].strip())
                    CURRENT_REGEX.set(r)
                    return True
        return False


class CmdHookPoint(HookPoint[typing.Union[CmdFullMatchHook, CmdRegexMatchHook]]):
    def add(self, cmd: str, func, regex=False):
        if regex:
            hook = CmdRegexMatchHook(cmd, func)
        else:
            hook = CmdFullMatchHook(cmd, func)
        self.hooks.append(hook)
