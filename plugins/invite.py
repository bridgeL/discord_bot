from core import App

app = App("invite")


@app.on_cmd("invite")
async def _():
    await app.send("请点击链接邀请我到你的服务器！ https://discord.com/api/oauth2/authorize?client_id=1132989755416653904&permissions=2419452944&scope=bot")
