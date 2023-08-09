import shlex
import discord
from pathlib import Path
from .hook import CmdHookPoint, Hook, HookPoint
from .context import CURRENT_MSG, CURRENT_TEXT, CURRENT_CMD, CURRENT_PREFIX, CURRENT_REGEX


class Bot:
    def __init__(self, token: str) -> None:
        self.token = token

        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        self.cmd_hook_point = CmdHookPoint()
        self.msg_hook_point = HookPoint()
        self.start_hook_point = HookPoint()

    # quick property

    @property
    def msg(self):
        return CURRENT_MSG.get()

    @property
    def cid(self):
        return self.msg.channel.id

    @property
    def uid(self):
        return self.msg.author.id

    @property
    def uname(self):
        return self.msg.author.display_name

    @property
    def cmd(self):
        return CURRENT_CMD.get()

    @property
    def prefix(self):
        return CURRENT_PREFIX.get()

    @property
    def text(self):
        return CURRENT_TEXT.get()

    @property
    def regex(self):
        return CURRENT_REGEX.get()

    @property
    def args(self):
        return shlex.split(self.text)

    # on_xxx decorator

    def on_cmd(self, cmd: str):
        def decorator(func):
            self.cmd_hook_point.add(cmd, func)
            return func
        return decorator

    def on_regex(self, cmd: str):
        def decorator(func):
            self.cmd_hook_point.add(cmd, func, True)
            return func
        return decorator

    def on_msg(self):
        def decorator(func):
            h = Hook(func)
            self.msg_hook_point.hooks.append(h)
            return func
        return decorator

    def on_start(self, func):
        h = Hook(func)
        self.start_hook_point.hooks.append(h)
        return func

    # important function

    async def send(self, text: str, cid=0, uid=0):
        if cid:
            channel = await self.client.fetch_channel(cid)
            await channel.send(text)  # type: ignore
        elif uid:
            user = await self.client.fetch_user(uid)
            await user.send(text)  # type: ignore
        else:
            channel = self.msg.channel
            await channel.send(text)

    def run_forever(self):
        self.client.run(self.token)


TOKEN = Path("token.txt").read_text("utf8")
bot = Bot(TOKEN)


@bot.client.event
async def on_message(msg: discord.message.Message):
    print(msg.channel, msg.author.name, msg.content)

    # exclude self
    if msg.author == bot.client.user:
        return

    CURRENT_MSG.set(msg)
    await bot.cmd_hook_point.run(msg.content)
    await bot.msg_hook_point.run()


@bot.client.event
async def on_ready():
    print(f'We have logged in as {bot.client.user}')
    await bot.start_hook_point.run()
