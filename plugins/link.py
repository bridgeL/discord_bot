from core import App

app = App("link")

urls = '''
Student Links: 
ANU ISIS: https://isis.anu.edu.au/ 
Wattle: https://wattlecourses.anu.edu.au/my/ 
Student Email: https://outlook.com/owa/anu.edu.au 
'''.strip()


@app.on_cmd("link")
async def _():
    await app.send(urls)
