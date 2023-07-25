from core import App

app = App("bkss")


@app.on_regex("^[Bb][Kk][Ss][Ss]")
async def _():
    await app.send("位置：student center level 2\n时间：8:30-10:30供应免费早餐")
