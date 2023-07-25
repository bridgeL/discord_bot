from core import App

app = App("hello")


@app.on_cmd("hello")
async def _():
    await app.send("world!")
