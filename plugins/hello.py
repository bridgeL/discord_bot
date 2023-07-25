from core import App

app = App("hello")


@app.on_cmd("hello")
async def _():
    await app.send("world!")
    await app.send(f"you can review my code here！ https://github.com/bridgeL/discord_bot")
