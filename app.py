from flask import Flask, render_template, request, redirect, url_for, session, send_file
import requests
import asyncio
import aiohttp
import random
import time

import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
# import ssl
# from flask_session import Session
# ssl._create_default_https_context = ssl._create_unverified_context

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


def save_users_to_session(users):
    users_list_to_save = []
    for user in users:
        user_dict = {}
        user_dict['sprites'] = {}
        user_dict['sprites']['front_default'] = user['sprites']['front_default']
        user_dict['name'] = user['name']
        user_dict['height'] = user['height']
        user_dict['weight'] = user['weight']
        users_list_to_save.append(user_dict)
    session['users'] = users_list_to_save


async def fetch_url(client_session, url):
    """Fetch the specified URL using the aiohttp session specified."""
    # response = await session.get(url)
    async with client_session.get(url, ssl=False) as resp:
        response = await resp.json()
        return response


async def get_all_urls(from_val, until_val):
    async with aiohttp.ClientSession(trust_env=True) as client_session:
        tasks = []
        for i in range(from_val, until_val):
            url = f'https://pokeapi.co/api/v2/pokemon/{i}'
            task = asyncio.create_task(fetch_url(client_session, url))
            tasks.append(task)
        data = await asyncio.gather(*tasks)
    return data


def get_users_sync(from_val, until_val):
    users = []
    for i in range(from_val, until_val):
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
            print('run')

            # asyncio.set_event_loop(asyncio.new_event_loop())
            # loop = asyncio.get_event_loop()
            # users = loop.run_until_complete(get_all_urls(from_val, until_val))
            # print('event loop')

        end_time = time.time()
        time_to_finish = f'{end_time - start_time: .2f} seconds'
        session[f'{request.args["type"]}_time'] = time_to_finish
        session[f'{request.args["type"]}_num'] = session['num']
        save_users_to_session(users)
        return render_template('users.html',
                               users=users,
                               time=time_to_finish,
                               from_val=from_val, until_val=until_val,
                               type_req=request.args['type'])
    else:
        pass
        # users = session['users']
        session.clear()
        # session['users'] = users
        return render_template('users.html')


@app.route('/rand_users')
def rand_users_func():
    num = int(request.args['num'])
    start = random.randint(1, 100)
    params = {'from': start, 'until': start + num, 'type': request.args['type']}
    return redirect(url_for('users_func', **params))


@app.route('/fetch')
def fetch_func():
    return render_template('fetch_example.html')


@app.route('/graphs')
def graphs_func():
    range_num = 10
    if 'range_num' in request.args:
        range_num = int(request.args['range_num'])
    return render_template('graphs.html', range_num=range_num)


@app.route('/get_image')
def get_image_func():
    num = int(request.args['num'])
    plt.clf()
    y = np.sin(np.array(range(num)))
    y *= 10 * np.random.rand()
    # print(y)
    plt.plot(y)
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png', cache_timeout=0,)



if __name__ == '__main__':
    app.run(debug=True)
