from flask import Flask, render_template, request, redirect, url_for, session
import requests
import asyncio
import aiohttp
import random
import time


app = Flask(__name__)
app.secret_key = '123'
data_list_sync = []
data_list_async = []


async def async_get_data(name):
    await asyncio.sleep(5)
    data_list_async.append(name)
    return f'Input value: {data_list_async} '


@app.route("/data")
async def get_data():
    tasks = []
    for i in range(10):
        task = asyncio.create_task(async_get_data(i))
        tasks.append(task)
    data = await asyncio.gather(*tasks)
    return render_template('async_check.html', data=data)


def get_data_func_internal(name):
    time.sleep(5)
    data_list_sync.append(name)
    return f'Input value: {data_list_sync} '


@app.route("/data_sync")
def get_data_sync():
    for i in range(10):
        get_data_func_internal(i)
    data = ''
    return render_template('async_check.html', data=data)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', data_sync=data_list_sync, data_async=data_list_async)


@app.route('/req')
def req_func():
    res = requests.get('https://api.github.com')
    res = requests.get('https://api.github.com/emojis', timeout=(2, 5))
    res = requests.post('https://httpbin.org/post', data={'key': 'value'}, timeout=1)
    # if res.status_code == 200:
    #     return f'Yes! status: {res.status_code}'
    # elif res.status_code == 404:
    #     return f'No! status: {res.status_code}'
    if res:
        res_json = res.json()
        return f'Yes! status: {res.status_code} | text: {res.json()}'
    else:
        return f'No! status: {res.status_code}'


async def fetch_url(client_session, url):
    """Fetch the specified URL using the aiohttp session specified."""
    # response = await session.get(url)
    async with client_session.get(url) as resp:
        response = await resp.json()
        return response


async def get_all_urls(from_val, until_val):
    async with aiohttp.ClientSession() as client_session:
        tasks = []
        for i in range(from_val, until_val + 1):
            url = f'https://pokeapi.co/api/v2/pokemon/{i}'
            task = asyncio.create_task(fetch_url(client_session, url))
            tasks.append(task)
        data = await asyncio.gather(*tasks)
    return data


def get_users_sync(from_val, until_val):
    users = []
    for i in range(from_val, until_val + 1):
        res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}')
        print(res)
        users.append(res.json())
    return users


@app.route('/users')
def users_func():
    if 'type' in request.args:
        start_time = time.time()
        from_val, until_val = int(request.args['from']), int(request.args['until'])
        session['num'] = until_val - from_val
        users = []

        # SYNC
        if request.args['type'] == 'sync':
            users = get_users_sync(from_val, until_val)

        # ASYNC
        if request.args['type'] == 'async':
            users = asyncio.run(get_all_urls(from_val, until_val))

        end_time = time.time()
        time_to_finish = f'{end_time - start_time: .2f} seconds'
        session[f'{request.args["type"]}_time'] = time_to_finish
        session[f'{request.args["type"]}_num'] = session['num']
        return render_template('users.html',
                               users=users,
                               time=time_to_finish,
                               from_val=from_val, until_val=until_val,
                               type_req=request.args['type'])
    else:
        session.clear()
        return render_template('users.html')


@app.route('/rand_users')
def rand_users_func():
    num = int(request.args['num'])
    start = random.randint(1, 100)
    params = {'from': start, 'until': start + num, 'type': request.args['type']}
    return redirect(url_for('users_func', **params))


if __name__ == '__main__':
    app.run()
