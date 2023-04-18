import html

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

db = client["lab4"]
cur = db["users"]

app = FastAPI()


def genPage(text):
    page = f"""
    <html>
        <head>
            <title>NCS: Lab 4</title>
        </head>
        <body>
            <h1>{text}</h1>
        </body>
    </html>
    """
    return page


@app.get("/")
async def root():
    return HTMLResponse(content=genPage("This is web application for lab 4"), status_code=200)


@app.get("/echo")
async def echo(text: str):
    text = html.escape(text)
    return HTMLResponse(content=genPage(text), status_code=200)


@app.get("/add_user_data")
async def add_user_data(login: str, password: str, data: str):
    x = cur.insert_one({
        "login": login,
        "password": password,
        "data": data
    })

    if x.acknowledged:
        return HTMLResponse(content=genPage("Data was successfully added"), status_code=200)
    else:
        return HTMLResponse(content=genPage("Something went wrong"), status_code=500)


@app.get("/get_user_data")
async def get_user_data(login: str, password: str):
    query = {'login': login, 'password': password}
    data = cur.find(query)

    page = "User data:\n<ul>"
    for x in data:
        page += f"<li>{x['data']}</li>"
    page += "</ul>"
    return HTMLResponse(content=genPage(page), status_code=200)