# Learning Fetch, Requests, `asyncio` in Flask and Plotting Graphs in Flask

## Fetch

In js file:

```js
function myFunction() {
    fetch('https://reqres.in/api/users?page=2').then(
        response => response.json()
    ).then(
        responseOBJECT => createUsersList(responseOBJECT.data)
    ).catch(
        err => console.log(err)
    );
}


function createUsersList(users){
    console.log(users);
    const user = users[0];
    console.log(user);
    const curr_main = document.querySelector("main");
    for(let user of users){
        const section = document.createElement('section');
        section.innerHTML = `
        <img src="${user.avatar}" alt="Profile Picture"/>
        <div>
            <span>${user.first_name} ${user.last_name}</span>
            <br>
            <a href="mailto:${user.email}">Send Email</a>
        </div>
        `;
        curr_main.appendChild(section);
    }
}
```

In html file:

```html
...
<h3>User List: <button onclick="myFunction()">Click me</button></h3>

<main>

</main>
<script src="../static/js/fetch_example.js"></script>
...
```

## Requests

```python
@app.route('/req')
def req_func():
    res = requests.get('https://api.github.com')
    res = requests.get('https://api.github.com/emojis', timeout=(2, 5))
    res = requests.post('https://httpbin.org/post', data={'key': 'value'}, timeout=1)
    if res.status_code == 200:
        return f'Yes! status: {res.status_code}'
    elif res.status_code == 404:
        return f'No! status: {res.status_code}'
    if res:
        res_json = res.json()
        return f'Yes! status: {res.status_code} | text: {res.json()}'
    else:
        return f'No! status: {res.status_code}'
```

## Async in python

```python
import time
import asyncio

async def async_count(i):
    print(f"[{i}] Start")
    await asyncio.sleep(1)
    print(f"[{i}] Finish")

async def async_gather():
    tasks = []
    for i in range(3):
        tasks.append(asyncio.create_task(async_count(i)))
    await asyncio.gather(*tasks)

def main_2():
    asyncio.run(async_gather())

if __name__ == "__main__":
    s = time.time()
    main_2()
    elapsed = time.time() - s
    print(f"Executed in {elapsed:0.2f} seconds.")
```

## Async programming in Flask

Similar to the previous example.

## Plotting graphs in Flask

In app.py:

```python
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
```

In html file:
```html
<form action="/graphs" method="get">
    <input type="number" name="range_num">
    <input type="submit" value="Get Graph">
</form>
<img src="{{ url_for('get_image_func', num=range_num) }}" alt="">
```

## Credits

### `requests` package:
- [RealPython | requests](https://realpython.com/python-requests/)
- [w3schools | HTTP Request Methods](https://www.w3schools.com/tags/ref_httpmethods.asp)
- [Wikipedia | Request methods](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods)

### aiohttp:
- [blog | aiohttp](https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp)

### `asyncio` in Flask:
- [Flask | Using `async` and `await`](https://flask.palletsprojects.com/en/2.0.x/async-await/#other-event-loops)
- [stackoverflow | pip install flask[async]](https://stackoverflow.com/questions/30539798/zsh-no-matches-found-requestssecurity)
- [blog | Async in Flask 2.0](https://testdriven.io/blog/flask-async/)
- [blog | geekyhumans](https://geekyhumans.com/de/create-asynchronous-api-in-python-and-flask/)

### Graphs:
- [jetbrains | Creating Web Applications with Flask](https://www.jetbrains.com/help/pycharm/creating-web-application-with-flask.html#line_charts)
- [sof | BytesIO](https://stackoverflow.com/questions/42800250/difference-between-open-and-io-bytesio-in-binary-streams)
- [flask | flask.send_file](https://flask.palletsprojects.com/en/2.0.x/api/#flask.send_file)
- [mozilla | mime types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types#image_types)

### Bugs:

- [sof | ssl=False](https://stackoverflow.com/questions/63347818/aiohttp-client-exceptions-clientconnectorerror-cannot-connect-to-host-stackover)
