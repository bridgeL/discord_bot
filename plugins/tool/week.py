import datetime
from core import App

app = App("week")
app.help = "查看现在是第几周"

init_date = datetime.date(2023, 7, 24)


@app.on_cmd("week")
async def _():
    date = datetime.datetime.now().date()
    delta_d = (date - init_date).days
    week = delta_d // 7
    if week > 6:
        week -= 2
    await app.send(f"U R in week {week+1}")
