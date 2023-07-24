from core import on_regex, send, get_current_text


@on_regex("^[Bb][Kk][Ss][Ss]")
async def _():
    await send("位置：student center level 2\n时间：8:30-10:30供应免费早餐")
