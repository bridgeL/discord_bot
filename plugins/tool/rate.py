from core import App
import requests

app = App("rate")
app.help = "查询今日澳元汇率"

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


@app.on_cmd("rate")
async def _():
    await app.send("查询今日澳元汇率：稍等...正在请求百度API")
    res = requests.get(url=url, headers=headers, params=params)
    data = res.json()["data"][0]["info"]
    data = "\n".join(
        f"{d['name']} {d['value']},   趋势: {d['status']} " for d in data)
    await app.send(data)
