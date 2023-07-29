from core import App

app = App("user")


@app.on_cmd("user")
async def _():
    keys = app.bot.args
    if keys:
        await app.send(f"<https://discordapp.com/users/{keys[0]}>")
