import time

from flask import Flask, render_template, request
import asyncio

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run()
