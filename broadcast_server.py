import asyncio
import datetime
import functools
import websockets

def readDeviceData(packet):
    return "i'm reading data packet " + str(packet)

async def handler(websocket, path, extra_arg):
    if (extra_arg):
        await websocket.send(extra_arg)
    i=0
    while True:
        now = datetime.datetime.utcnow().isoformat()
        try:
            await websocket.send(now +' => '+readDeviceData(i))
        except Exception as e:
            if(e.code ==1005):
                print('A client is gone for some reason')
            print('Error!: ', e)
            break
        await asyncio.sleep(1)
        i+=1
        
bound_handler = functools.partial(handler, extra_arg='hello dear customer')
start_server = websockets.serve(bound_handler, "127.0.0.1", 5678)

print("Server has been started")
print("Broadcasting data ...")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()