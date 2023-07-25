from asyncio import sleep
from random import randint, seed
from time import time
from core import App
from .user import manager

app = App("bet")
app.help = '''
猜硬币 randint(0, 1)

`.bet 10 正` 使用10金，猜硬币是正面，获胜获得20金，失败颗粒无收

你也可以all in！

`.bet all 反` 
'''.strip()

seed(time())


@app.on_cmd("bet")
async def _():
    args = app.bot.args
    if not args:
        await app.send_help()
        return

    n = args[0]
    r = args[1]
    user = manager.get(app.bot.uid)

    if n == "all":
        n = user.money
    else:
        n = int(n)

    r = 0 if r == "反" else 1

    if n <= 0:
        await app.send(f"{app.bot.uname} 没钱不许参加")

    if r:
        await app.send(f"{app.bot.uname} 赌正！")
    else:
        await app.send(f"{app.bot.uname} 赌反！")

    await sleep(1)

    rr = randint(0, 1)
    if rr:
        await app.send("结果是正！")
    else:
        await app.send("结果是反！")

    if r == rr:
        user.money += n
        manager.save()
        await app.send(f"{app.bot.uname} 赢啦！净赚{n}金！目前财富：{user.money}金")
    else:
        user.money -= n
        manager.save()
        await app.send(f"{app.bot.uname} 输啦！扣除{n}金！目前财富：{user.money}金")
