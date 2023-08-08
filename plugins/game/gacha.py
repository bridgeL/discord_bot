from asyncio import sleep
from random import randint
from core import App
from .user import manager

app = App("gacha")
app.help = '''
花费金额抽卡，并按照奖励倍数返还！

`.gacha 10` 花费10金进行一次单抽！
`.gacha 100` 花费100金进行一次单抽！
`.gacha all` all in 进行一次单抽！

抽卡概率公示：

图标 获取概率 奖励倍数
💴   1%    100
💷   10%   10
💶   20%   5
💵   30%   1
<:_3:1133688423350292570>   39% 0
'''.strip()

gacha_icons = ["💴", "💷", "💶", "💵", "<:_3:1133688423350292570>"]
gacha_weight = [1, 10, 20, 30, 39]
gacha_reward = [100, 10, 5, 1, 0]


def get_one():
    d = randint(0, sum(gacha_weight) - 1)
    for i in range(len(gacha_weight)):
        if d < sum(gacha_weight[:i+1]):
            return i
    raise ValueError


@app.on_cmd("gacha")
async def _():
    args = app.bot.args
    if not args:
        await app.send_help()
        return

    n = args[0]
    user = manager.get(app.bot.uid)

    if n == "all":
        n = user.money
    else:
        n = int(n)

    if n <= 0 or n > 10000:
        await app.send(f"{app.bot.uname} 你小子")
        return

    if n > user.money:
        await app.send(f"{app.bot.uname} 没钱不许参加")
        return

    user.money -= n

    await app.send(f"{app.bot.uname} 花费{n}金 抽卡！")
    await sleep(1)

    d = get_one()
    await app.send(gacha_icons[d])

    reward = gacha_reward[d] * n
    user.money += reward
    manager.save()

    await app.send(f"{app.bot.uname} 获得{reward}金！目前财富：{user.money}金")
