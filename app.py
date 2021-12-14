from flask import Flask
import asyncio

app = Flask(__name__)


async def async_get_data():
    await asyncio.sleep(1)
    return 'Done!'


@app.route("/data")
async def get_data():
    data = await async_get_data()
    return data


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
