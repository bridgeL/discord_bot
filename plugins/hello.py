from core import App

app = App("hello")


@app.on_cmd("hello")
async def _():
    await app.send("world!")
    await app.send(f"you can review my code here！ https://github.com/bridgeL/discord_bot")
    await app.send("you can also develop funny or useful plugins and contribute them to this repo!!! THANKS TO EVERY SUPPORT")
