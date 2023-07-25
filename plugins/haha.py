from core import App

app = App("haha")


@app.on_regex(r"(ha)+")
async def _():
    n = len(app.bot.regex.group()) // 2
    d = "笑"*n
    await app.send(f"不许{d}了")
