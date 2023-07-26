from core import App
import requests
from table2ascii import table2ascii as t2a, PresetStyle

app = App("rate")
app.help = "查询今日澳元汇率 `.rate` / `.汇率`"

url = "https://finance.pae.baidu.com/async"
headers = {}
params = {
    "srcid": "50494",
    "group": "huilv_minute",
    "tab_id": "5",
    "query": "AUDCNY",
    "all": "1",
    "isIndex": "false",
    "isBk": "false",
    "isBlock": "false",
    "isStock": "false",
    "isFutures": "false",
    "isForeign": "true",
    "code": "AUDCNY",
    "stockType": "global",
    "newFormat": "1",
    "finClientType": "pc",
}


@app.on_cmd("汇率")
@app.on_cmd("rate")
async def _():
    await app.send("查询今日澳元汇率：稍等...")
    res = requests.get(url=url, headers=headers, params=params)
    data = res.json()["data"][0]["info"]
    for d in data:
        d.pop("ename")
        d["name"] = d["name"][:-1]
        # d.pop("name")

    output = t2a(
        header=list(data[0].keys()),
        body=[list(d.values()) for d in data],
        style=PresetStyle.thin_compact
    )

    await app.send(f"```\n{output}\n```")
    await app.send("\n数据收集自百度")
