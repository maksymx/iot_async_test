from aiohttp import web, MsgType


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.tp == MsgType.text:
            if msg.data == 'close':
                await ws.close()
            else:
                ws.send_str(msg.data)
        elif msg.tp == MsgType.error:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


app = web.Application()
app.router.add_route('GET', '/websocket', websocket_handler)

if __name__ == "__main__":
    web.run_app(app)
