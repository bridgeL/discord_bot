from core import App

app = App("link")

urls = '''
Student Links: 
ANU ISIS: https://isis.anu.edu.au/ 
Wattle: https://wattlecourses.anu.edu.au/my/
Student Email: https://outlook.office365.com/mail/
Timetable: https://www.anu.edu.au/students/program-administration/timetabling/student-access-and-support-for-mytimetable
'''.strip()


@app.on_cmd("link")
async def _():
    await app.send(urls)
