import aiohttp
import asyncio


async def websocket_client(*args, **kwargs):
    session = aiohttp.ClientSession()
    async with session.ws_connect('ws://127.0.0.1:8080/websocket') as ws:
        ws.send_str("Hello server")
        async for msg in ws:
            # print(">>>>>>>>", msg.data)
            if msg.tp == aiohttp.MsgType.text:
                if msg.data == 'close cmd':
                    await ws.close()
                    break
                else:
                    ws.send_str(msg.data)
                    asyncio.sleep(2)
            elif msg.tp == aiohttp.MsgType.binary:
                print('Binary: ', msg.data)
            elif msg.tp == aiohttp.MsgType.ping:
                ws.pong()
            elif msg.tp == aiohttp.MsgType.pong:
                print('Pong received')
            elif msg.tp == aiohttp.MsgType.closed:
                break
            elif msg.tp == aiohttp.MsgType.error:
                break


loop = asyncio.get_event_loop()
content = loop.run_until_complete(websocket_client())
print(content)
