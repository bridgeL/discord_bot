import json
import aiocron
from pathlib import Path
from core import on_start, on_cmd, send, get_current_args, get_cid


def _add(cron, name, desc, cid):
    @aiocron.crontab(cron, start=False)
    async def task():
        await send(f"[{name}]\n{desc}", cid=cid)
    return task


class Task:
    def __init__(self, cid, name, desc, cron: str) -> None:
        self.cid = cid
        self.name = name
        self.desc = desc
        self.cron = cron

    def dict(self):
        return {
            "cid": self.cid,
            "name": self.name,
            "desc": self.desc,
            "cron": self.cron
        }

    def start(self):
        self.task = _add(self.cron, self.name, self.desc, self.cid)
        self.task.start()

    def stop(self):
        self.task.stop()

    def __str__(self) -> str:
        cron = self.cron.replace("*", "\\*")
        return f'''[{self.name}]\n{self.desc}\ncron表达式: {cron}'''


class Manager:
    def __init__(self) -> None:
        self.path = Path(__file__).with_name("data.json")
        data = json.loads(self.path.read_text("utf8"))
        self.tasks = [Task(**d) for d in data]

    def start_all(self):
        for task in self.tasks:
            task.start()

    def get(self, name):
        cid = get_cid()
        for task in self.tasks:
            if task.cid == cid and task.name == name:
                return task

    def get_all(self):
        cid = get_cid()
        return [task for task in self.tasks if task.cid == cid]

    def save(self):
        data = [task.dict() for task in self.tasks]
        self.path.write_text(json.dumps(
            data, ensure_ascii=False, indent=4), "utf8")

    def add(self, name, desc, cron):
        task = self.get(name)
        if task:
            return

        task = Task(get_cid(), name, desc, cron)
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


@on_start
async def _():
    manager.start_all()


@on_cmd("list cron")
async def _():
    tasks = manager.get_all()
    for task in tasks:
        await send(str(task))


@on_cmd("add cron")
async def _():
    args = get_current_args()
    task = manager.add(*args)
    if task:
        await send(f"添加成功 {task}")
    else:
        await send("添加失败 存在重名任务")


@on_cmd("remove cron")
async def _():
    args = get_current_args()
    task = manager.remove(args[0])
    if task:
        await send(f"移除成功 {task}")
    else:
        await send("移除失败 不存在该任务")


@on_cmd("help cron")
async def _():
    await send('''=== cron 使用帮助 ===
               
添加定时任务
add cron [name] [desc] [cron]

移除定时任务
remove cron [name]

查看所有定时任务
list cron''')
