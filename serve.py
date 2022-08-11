import random
import string
from platform import system

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import run

from main.codemao import login

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

tokens = {}


@app.get('/')
async def root():
    file = open("static/index.html", 'r', encoding='utf-8')
    text = file.read()
    file.close()
    return HTMLResponse(text)


@app.get('/token/')
async def get_token(username: str, password: str):
    bcm = str(login(username, password))
    if bcm is not None and bcm not in tokens.keys():
        tokens[bcm] = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        data = {'result': 'success'}
        response = JSONResponse(content=data)
        response.set_cookie('id', str(bcm))
        response.set_cookie('token', tokens[bcm])
        print('set', bcm, tokens[bcm])
        return response
    else:
        data = {'result': 'failed'}
        response = JSONResponse(content=data)
        return response


@app.post('/login/')
async def post_login(identity: str = Form(...), token: str = Form(...)):
    print('ask', identity, token)
    print(tokens)

    def yes():
        print('yes')
        file = open("static/home.html", 'r', encoding='utf-8')
        text = file.read()
        file.close()
        return HTMLResponse(text)

    def no():
        print('no')
        file = open("static/error.html", 'r', encoding='utf-8')
        text = file.read()
        file.close()
        return HTMLResponse(text)

    if str(identity) in tokens.keys():
        if tokens[str(identity)] == token:
            return yes()
        else:
            return no()
    else:
        return no()


if __name__ == '__main__' and system().lower() != 'linux':
    run(app, host='127.0.0.1', port=8000, debug=True)
