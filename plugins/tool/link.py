import discord
from core import App

app = App("link")


embed = discord.Embed(
    title="Student Links",
    description="- [ANU ISIS](https://isis.anu.edu.au/)\n- [Wattle](https://wattlecourses.anu.edu.au/my/)\n- [Student Email](https://outlook.office365.com/mail/)\n- [Timetable](https://www.anu.edu.au/students/program-administration/timetabling/student-access-and-support-for-mytimetable)",
    color=0xFF5733
)


@app.on_cmd("link")
async def _():
    await app.channel.send(embed=embed)
