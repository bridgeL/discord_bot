import json
import requests
import discord
from random import sample
from pathlib import Path
from core import App


app = App("course")
app.help = '''课程查询

- 基本使用 `-cp [name or code]` （默认postgraduate、2023年、s1+s2学期、COMP+MATH领域）
- 查询指定年份 `-cp [name or code] -y 2023`
- 查询指定学期 `-cp [name or code] [-s1] [-s2]`
- 查询指定领域 `-cp [name or code] -d comp math`
- 查询指定学历 `-cp [name or code] [-u] [-p]`'''


def get(y="2023", s1=False, s2=False, u=False, p=False, d=["comp", "math"], name=""):
    url = "https://programsandcourses.anu.edu.au/data/CourseSearch/GetCourses"
    params = {
        "AppliedFilter": "FilterByCourses",
        "Source": "",
        "ShowAll": "true",
        "PageIndex": "0",
        "MaxPageSize": "10",
        "PageSize": "Infinity",
        "SortColumn": "",
        "SortDirection": "",
        "InitailSearchRequestedFromExternalPage": "false",
        "SearchText": name,
        "SelectedYear": y,
        "Careers[0]": "Undergraduate" if u else "",
        "Careers[1]": "Postgraduate" if p else "",
        "Careers[2]": "",
        "Careers[3]": "",
        "Sessions[0]": "",
        "Sessions[1]": "First Semester" if s1 else "",
        "Sessions[2]": "",
        "Sessions[3]": "",
        "Sessions[4]": "Second Semester" if s2 else "",
        "Sessions[5]": "",
        "DegreeIdentifiers[0]": "Single",
        "DegreeIdentifiers[1]": "",
        "DegreeIdentifiers[2]": "",
        "FilterByMajors": "",
        "FilterByMinors": "",
        "FilterBySpecialisations": "",
        "CollegeName": "",
        "ModeOfDelivery": "In Person",
    }

    res = requests.get(url=url,  params=params)
    _data = res.json()["Items"]

    d = [_.lower() for _ in d]

    data = []
    for _d in _data:
        code = _d["CourseCode"].lower()
        if code.startswith(tuple(d)):
            data.append(_d)

    return data


@app.on_cmd("cp")
async def _():
    items = app.bot.args
    args = []
    kwargs = {}
    k = ""
    for item in items:
        if not k:
            if item.startswith("-"):
                k = item.lstrip("-")
            else:
                args.append(item)
        else:
            if item.startswith("-"):
                kwargs[k] = True
                k = item.lstrip("-")
            else:
                if k not in kwargs:
                    kwargs[k] = item
                else:
                    if not isinstance(kwargs[k], list):
                        kwargs[k] = [kwargs[k]]
                    kwargs[k].append(item)
    if k and k not in kwargs:
        kwargs[k] = True

    if "s1" not in kwargs and "s2" not in kwargs:
        kwargs["s1"] = True
        kwargs["s2"] = True

    if "u" not in kwargs and "p" not in kwargs:
        kwargs["p"] = True

    kwargs["name"] = " ".join(args)

    data = get(**kwargs)

    if not data:
        await app.send("没有查到相关课程")
        await app.send_help()
        return

    if len(data) > 20:
        await app.send("搜索到超过20条结果，仅随机展示其中的20条，如想获得进一步信息，请细化你的搜索关键词")
        data = sample(data, 20)

    data.sort(key=lambda d: d["CourseCode"])

    if len(data) > 5:
        t = "\n".join(d["CourseCode"] + " " + d["Name"] for d in data)
        await app.send(f"搜索到相关课程：\n{t}\n如需进一步信息请查询完整名称")
        return

    s = ""
    for d in data:
        link = f"https://programsandcourses.anu.edu.au/{d['Year']}/course/{d['CourseCode']}"
        ss = f"- 课程年份：{d['Year']}\n- 课程代码：[{d['CourseCode']}]({link})\n- 课程学历：{d['Career']}\n"
        s += f"{ss}- 课程名称：{d['Name']}\n- 课程时间：{d['Session']}\n"

        _d = find(d["CourseCode"])
        if _d:
            classes = _d["classes"]
            __d = {}
            for cls in classes:
                __d.setdefault(cls["locationID"], [])
                __d[cls["locationID"]].append(cls["location"])

            ss = ""
            for k, v in __d.items():
                v = list(set(v))
                v.sort()
                vv = ", ".join(v)
                if k:
                    ss += f"\n  - [{vv}]({k})"
                else:
                    ss += f"\n  - {vv}"

            s += f"- 课程位置：{ss}\n"

        s += "\n"

    description = s.strip()

    embed = discord.Embed(
        title="课程查询",
        description=description,
        color=0xFF5733
    )

    await app.channel.send(embed=embed)


def get_data():
    data1 = Path(__file__).with_name("2023.S1.json").read_text("utf8")
    data2 = Path(__file__).with_name("2023.S2.json").read_text("utf8")
    data: dict = json.loads(data1)
    data.update(json.loads(data2))
    return data


def find(k):
    k = k.lower()
    for v in DATA.values():
        t = v["id"].lower()
        if k in t:
            return v


DATA = get_data()
