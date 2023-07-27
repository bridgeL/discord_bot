import json
from random import sample
import discord
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


def find_all(keys):
    keys = [k.lower() for k in keys]
    r = []
    for v in data.values():
        t = v["title"].lower()
        for k in keys:
            if k not in t:
                break
        else:
            r.append(v)

    return r


data = get_data()


@app.on_cmd("course")
async def _():
    keys = app.bot.args
    if not keys:
        await app.send_help()
        return

    data = find_all(keys)

    if not data:
        await app.send("没有查到相关课程")
        return

    if len(data) > 20:
        await app.send("搜索到超过20条结果，仅随机展示其中的20条，如想获得进一步信息，请细化你的搜索关键词")
        data = sample(data, 20)

    data.sort(key=lambda d: d["title"])

    if len(data) > 5:
        t = "\n".join(d["title"] for d in data)
        await app.send(f"搜索到相关课程：\n{t}\n如需进一步信息请查询完整名称")
        return

    s = ""
    for d in data:
        s += f"- 课程代码：[{d['id']}]({d['link']})\n- 课程名称：{d['title'][len(d['id'])+1:]}\n- 课程时间：{d['dates'].replace('Displaying Dates: ', '')}\n"
    description = s[:-1]

    embed = discord.Embed(
        title="课程查询",
        description=description,
        color=0xFF5733
    )

    await app.channel.send(embed=embed)
