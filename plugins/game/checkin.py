from core import App
from datetime import datetime
from .user import manager

app = App("checkin")


@app.on_cmd("checkin")
async def _():
    user = manager.get(app.bot.uid)
    date = str(datetime.now().date())
    if user.checkin_date == date:
        await app.send(f"{app.bot.uname} 已经签过到了，请明天再来")
        return

    user.checkin_date = date
    user.money += 100
    manager.save()
    await app.send(f"{app.bot.uname} 签到成功，获得100金\n目前财富：{user.money}金")
