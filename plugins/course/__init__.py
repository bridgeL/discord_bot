import json
from pathlib import Path
from core import App

app = App("course")
app.help = '''输入课程名称或代码查询详细内容，数据内容搜集自2023年'''


def get_data():
    data1 = Path(__file__).with_name("2023.S1.json").read_text("utf8")
    data2 = Path(__file__).with_name("2023.S2.json").read_text("utf8")
    data: dict = json.loads(data1)
    data.update(json.loads(data2))

    # pop classes
    for d in data.values():
        d.pop("classes")

    return data


def find_all(key):
    return [v for v in data.values() if key in v["title"]]


data = get_data()


@app.on_cmd("course")
async def _():
    key = app.bot.text
    if not key:
        await app.send_help()
        return

    data = find_all(key)

    if not data:
        await app.send("没有查到相关课程")
        return

    if len(data) > 1:
        t = "\n".join(d["title"] for d in data)
        await app.send(f"搜索到相关课程：\n{t}\n如需进一步信息请查询完整名称")
        return

    data = data[0]

    await app.send(f"""课程名称：{data['title'][len(data['id'])+1:]}
课程ID: {data['id']}
课程链接: {data['link']}
课程时间：{data['dates'].replace('Displaying Dates: ', '')}""")
