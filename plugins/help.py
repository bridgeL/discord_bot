from core import App
from core.app import ALL_APPS

app = App("help")


@app.on_cmd("help")
async def _():
    name = app.bot.text
    if not name:
        text = "欢迎使用全局帮助，所有功能模块名如下\n" + \
            "\n".join(_app.name for _app in ALL_APPS) + \
            "\n若想查看指定功能模块的详细帮助，请使用`.help [功能模块名]`"
        await app.send(text)
    else:
        for _app in ALL_APPS:
            if _app.name == name:
                await app.send(f"=== {name} 使用帮助 ===\n\n{_app.help}")
                return
        else:
            await app.send("没有找到该功能模块")
