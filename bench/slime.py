from slimeweb import Slime

app = Slime(__file__)


@app.websocket(path="/chat", method="GET")
def chatty(req, resp):

    def read_me(msg):
        if not resp.is_closed():
            resp.send(msg)

    resp.on_message(read_me)

    def close_me():
        pass

    resp.on_close(close_me)


@app.route(path="/plain", method="GET")
def land_plain(req, resp):
    return resp.plain("hello world")


@app.route(path="/json", method="GET")
def land_json(req, resp):
    return resp.json({"name": "abilash", "slimeversion": "V0.1.3"})


@app.route(path="/render", method="GET")
def land_render(req, resp):
    html = req.render(
        "hello.html",
        **{"name": "abilash", "SlimeVersion": "V0.1.3"},
    )
    return resp.html(html)


@app.route(path="/", method="GET")
def land(req, resp):
    counter = req.get_state("counter")
    html = req.render(
        "hello.html",
        **{"name": "abilash", "SlimeVersion": "V0.1.3", "counter": counter},
    )
    req.update_state("counter", counter + 1)
    return resp.html(html)


@app.middle_after(path="/", method="GET")
async def land_after(req, resp):
    resp.set_header("BEFORE", "Request")


@app.middle_before(path="/", method="GET")
async def land_before(req, resp):
    resp.set_header("AFTER", "REQUEST")


@app.route(path="/stream", method="GET", stream="text/plain")
async def stream_me(req, resp):
    await asyncio.sleep(1)
    resp.start_stream()
    for i in range(5):
        resp.send(i)
    resp.close()


@app.route(path="/test", method="POST")
def hello(req, resp):
    for file in req.file:
        print(file.filename)
        print(file.content_type)
        print(file.file_path)
        print(file.file_size)
        print(file.extension)
        file.save(f"./testing_file.{file.extension}")
    return resp.json({"status": "ok"})


if __name__ == "__main__":
    app.serve(app_state={"counter": 0})
