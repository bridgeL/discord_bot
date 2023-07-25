import json
import aiocron
from pathlib import Path
from core import App

app = App("cron")
app.help = '''
本定时任务应用最高精度为1分钟，请不要设置秒级精度的cron

添加定时任务
add [name] [desc] [cron]

移除定时任务
remove [name]

查看所有定时任务
list

退出管理界面
exit

注意：包含空格的[name],[desc],[cron]请使用""包裹，例如：

`.add "test 1" 仅在星期二有效；从第1分钟开始，每10分钟触发一次 "1/10 * * * 2"`

cron语法规则：https://help.aliyun.com/document_detail/133509.html
'''.strip()


class Task:
    def __init__(self, cid, name, desc, cron: str, uid) -> None:
        self.cid = cid
        self.name = name
        self.desc = desc
        self.cron = cron
        self.uid = uid

    def dict(self):
        return {
            "cid": self.cid,
            "name": self.name,
            "desc": self.desc,
            "cron": self.cron,
            "uid": self.uid
        }

    def start(self):
        @aiocron.crontab(self.cron, start=False)
        async def timer():
            await app.send(f"定时任务提醒 [{self.name}]\n{self.desc}", cid=self.cid)
        self.timer = timer
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def __str__(self) -> str:
        return f'''[{self.name}]\n{self.desc}\ncron: `{self.cron}`\n添加者：https://discordapp.com/users/{self.uid}'''


class Manager:
    def __init__(self) -> None:
        self.path = Path(__file__).with_name("data.json")

        if not self.path.exists():
            with self.path.open("w+", encoding="utf8") as f:
                f.write("[]")

        data = json.loads(self.path.read_text("utf8"))
        self.tasks = [Task(**d) for d in data]

    def start_all(self):
        for task in self.tasks:
            task.start()

    def get(self, name):
        cid = app.bot.cid
        for task in self.tasks:
            if task.cid == cid and task.name == name:
                return task

    def get_all(self):
        cid = app.bot.cid
        return [task for task in self.tasks if task.cid == cid]

    def save(self):
        data = [task.dict() for task in self.tasks]
        self.path.write_text(json.dumps(
            data, ensure_ascii=False, indent=4), "utf8")

    def add(self, name, desc, cron):
        task = self.get(name)
        if task:
            return

        task = Task(app.bot.cid, name, desc, cron, app.bot.uid)
        self.tasks.append(task)
        task.start()
        self.save()
        return task

    def remove(self, name):
        task = self.get(name)
        if not task:
            return
        self.tasks.remove(task)
        task.stop()
        self.save()
        return task


manager = Manager()


@app.bot.on_start
async def _():
    manager.start_all()


@app.on_cmd("cron")
async def _():
    app.state = "cron"
    await app.send("已进入cron管理界面")
    await app.send_help()


@app.on_cmd("exit", "cron")
async def _():
    app.state = ""
    await app.send("已退出cron管理界面")


@app.on_cmd("list", "cron")
async def _():
    tasks = manager.get_all()
    if not tasks:
        await app.send("目前没有任何定时任务，使用add命令来添加一个吧！")
        return

    for task in tasks:
        await app.send(str(task))


@app.on_cmd("add", "cron")
async def _():
    task = manager.add(*app.bot.args)
    if task:
        await app.send(f"添加成功 {task}")
    else:
        await app.send("添加失败 存在重名任务")


@app.on_cmd("remove", "cron")
async def _():
    name = app.bot.args[0]
    task = manager.remove(name)
    if task:
        await app.send(f"移除成功 {task}")
    else:
        await app.send(f"移除失败 不存在任务 [{name}]")
