import random
import string
from platform import system

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from uvicorn import run

from main.codemao import login
from main.core import *

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

tokens = {}

court = Court()
court.events.append(Event('Test', time.time(), 'None'))

template = Jinja2Templates(directory='static')


@app.get('/')
async def root():
    print('get', 'Page', 'index.html')
    return HTMLResponse(login_html())


@app.get('/token/')
async def get_token(username: str, password: str):
    print('get', 'string', 'token')
    bcm = login(username, password)
    if bcm is not None and bcm not in tokens.keys():
        tokens[bcm] = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        data = {'result': 'success'}
        response = JSONResponse(content=data)
        response.set_cookie('id', str(bcm))
        response.set_cookie('token', tokens[bcm])
        print('···', 'set', bcm, tokens[bcm])
        return response
    else:
        data = {'result': 'failed'}
        response = JSONResponse(content=data)
        print('···', 'failed')
        return response


@app.post('/hall/')
async def post_login(identity: str = Form(...), token: str = Form(...)):
    print('post', 'form', 'login')
    print('···', 'ask', identity, token)

    def yes():
        print('···', '···', 'yes')
        return HTMLResponse(court.html())

    def no():
        print('···', '···', 'no')
        return HTMLResponse('failed')

    if str(identity) in tokens.keys():
        if tokens[str(identity)] == token:
            return yes()
        else:
            return no()
    else:
        return no()


@app.get('/{number}')
async def get_vote(number: int):
    print('get', 'page', 'event:', number)
    return HTMLResponse(court.events[number - 1].html())


if __name__ == '__main__' and system().lower() != 'linux':
    run(app, host='127.0.0.1', port=8000)
