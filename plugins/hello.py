from core import App

app = App("hello")


@app.on_cmd("hello")
async def _():
    await app.send("world!")
    await app.send("you can review my code here！ https://github.com/bridgeL/discord_bot\nyou can also develop funny or useful plugins and contribute them to this repo!!! \nTHANKS TO EVERY SUPPORT")
