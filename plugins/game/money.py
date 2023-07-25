from core import App
from .user import manager

app = App("game/money")


@app.on_cmd("money")
async def _():
    user = manager.get(app.bot.uid)
    await app.send(f"{app.bot.uname} 目前财富：{user.money}金")
