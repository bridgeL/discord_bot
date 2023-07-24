import re
import shlex
import discord
import asyncio
from typing import List
from pathlib import Path
from contextvars import ContextVar
from importlib import import_module


def load_all_plugins():
    for p in Path("plugins").iterdir():
        if p.stem.startswith(("_", ".")):
            continue
        name = ".".join(p.with_suffix("").parts)
        try:
            import_module(name)
        except:
            print(f"{name} 导入失败 X")
        else:
            print(f"{name} 导入成功")


CURRENT_MSG: ContextVar[discord.message.Message] = ContextVar("CURRENT_MSG")
CURRENT_TEXT: ContextVar[str] = ContextVar("CURRENT_TEXT")

PREFIXES = ["$", "."]


class Hook:
    def __init__(self) -> None:
        self.func = None

    def check(self, text: str) -> bool:
        raise NotImplementedError


MSG_HOOKS: List[Hook] = []


class FullMatchHook(Hook):
    def __init__(self, cmd: str, func) -> None:
        self.cmd = cmd
        self.func = func

    def check(self, text: str):
        for prefix in PREFIXES:
            p = prefix+self.cmd
            if text.startswith(p):
                CURRENT_TEXT.set(text[len(p):].strip())
                return True
        return False


class RegHook(Hook):
    def __init__(self, patt: re.Pattern, func) -> None:
        self.patt = patt
        self.func = func

    def check(self, text: str) -> bool:
        for prefix in PREFIXES:
            if text.startswith(prefix):
                text = text[len(prefix):]
                r = self.patt.search(text)
                if r:
                    CURRENT_TEXT.set(text[r.span()[1]:].strip())
                    return True
        return False


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def get_client():
    return client


START_HOOKS = []


def on_start(func):
    START_HOOKS.append(func)
    return func


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    for func in START_HOOKS:
        asyncio.create_task(func())


async def send(text: str, cid=0):
    if cid:
        c = client.get_channel(cid)
        await c.send(text)
        return

    msg = CURRENT_MSG.get()
    await msg.channel.send(text)


def get_current_text():
    return CURRENT_TEXT.get()


def get_current_args():
    return shlex.split(get_current_text())


def get_cid():
    return CURRENT_MSG.get().channel.id


def on_cmd(cmd: str):
    def decorator(func):
        MSG_HOOKS.append(FullMatchHook(cmd, func))
        return func
    return decorator


def on_regex(patt_str: str):
    def decorator(func):
        MSG_HOOKS.append(RegHook(re.compile(patt_str), func))
        return func
    return decorator


@client.event
async def on_message(msg: discord.message.Message):
    CURRENT_MSG.set(msg)

    # exclude self
    if msg.author == client.user:
        return

    for hook in MSG_HOOKS:
        if hook.check(msg.content):
            asyncio.create_task(hook.func())


def run():
    client.run(Path("token.txt").read_text("utf8"))
