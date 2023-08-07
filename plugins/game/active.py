import aiocron
from core import App
from .user import manager

app = App("active")
app.help = '''
每日活跃度奖励

根据发言次数增加财富，每天0点静默结算
'''.strip()


@aiocron.crontab("0 0 * * *")
async def timer():
    for user in manager.users:
        print(user.uid, user.msg_cnt)
        user.money += user.msg_cnt
        user.msg_cnt = 0
    manager.save()
    print("已结算当日活跃度奖励")


@app.bot.on_msg()
async def _():
    user = manager.get(app.bot.uid)
    user.msg_cnt += 1
    manager.save()
