from core import on_cmd, send


@on_cmd("hello")
async def _():
    await send("world!")


@on_cmd("invite")
async def _():
    await send("https://discord.com/api/oauth2/authorize?client_id=1132989755416653904&permissions=2419452944&scope=bot")
