import random
import string

from fastapi import FastAPI, Form, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from uvicorn import run

from main.codemao import login
from main.core import *
from main.image_test import *

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

tokens = {}
block_list = []

court = Court()
court.events.append(Event('Test', time.time(), '这仅仅是一条测试', len(court.events)))
court.events[-1].images.append(img1)
court.events[-1].images.append(img2)
court.events[-1].images.append(img3)
court.events[-1].votes.append(Vote('简与不简', time.time()))
court.events[-1].votes.append(Vote('还是简与不简', time.time()))
template = Jinja2Templates(directory='static')


@app.get('/')
async def root(request: Request):
    if request.client.host in block_list:
        return 404
    print('get', 'Page', 'index.html')
    return HTMLResponse(login_html())


@app.get('/token/')
async def get_token(request: Request, username: str, password: str):
    if request.client.host in block_list:
        return 404
    print('get', 'string', 'token')
    bcm = login(username, password)
    if bcm is not None:
        if bcm not in tokens.keys():
            tokens[bcm] = str().join(random.sample(string.ascii_letters + string.digits, 16))
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
async def post_login(request: Request, identity: str = Form(...), token: str = Form(...)):
    if request.client.host in block_list:
        return 404
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
async def get_vote(request: Request, id=Cookie(None), number: int = 1):
    if request.client.host in block_list:
        return 404
    print('get', 'page', 'event:', number - 1)
    return HTMLResponse(court.events[number - 1].html(id))


@app.get('/vote/')
async def get_result(request: Request, id=Cookie(None), event: str = '', name: str = '', value: str = ''):
    if request.client.host in block_list:
        return 404

    print('get', 'vote', event, name)
    if id in tokens.keys():
        e = court.events[int(event)]
        l = [i.object for i in e.votes]
        c = l.index(name)

        def val(value: str) -> Optional[bool]:
            if value == 'penalize':
                return True
            elif value == 'waiver':
                return None
            else:
                return False

        e.votes[c].ballots.append(Ballot(id, val(value)))
        print([i.value for i in e.votes[c].ballots])
    else:
        block_list.append(request.client.host)


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
