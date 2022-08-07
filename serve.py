from fastapi import FastAPI, Form
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from main.codemao import login

import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def root():
    file = open("static/index.html", 'r', encoding='utf-8')
    text = file.read()
    file.close()
    return HTMLResponse(text)


@app.post('/home/')
async def home(request: Request, username: str = Form(...), password: str = Form(...)):
    if login(int(username), password):
        file = open("static/home.html", 'r', encoding='utf-8')
        text = file.read()
        file.close()
        return HTMLResponse(text)
    else:
        return False


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
