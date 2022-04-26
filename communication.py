import asyncio
import websockets

async def echo(websocket):
    while True:
        try:
            await websocket.send('get outputs')
            received = await websocket.recv()
            print(received.split(',')[1])
            return int(received.split(',')[1])
        except:
            print('System not active...')
                

async def communication():
    async with websockets.serve(echo, "localhost", 6660):
        await asyncio.Future() 

asyncio.run(communication())
