"""May chu cam bien, cap nhat nhiet do va do am moi 3 giay."""
import argparse
import asyncio
import json
import random

import aiocoap
from aiocoap import resource


class Sensor(resource.Resource):
    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.temperature, self.humidity = 28.5, 65.2

    async def render_get(self, request):
        data = {"device_id": self.device_id, "temperature": self.temperature, "humidity": self.humidity}
        return aiocoap.Message(code=aiocoap.Code.CONTENT, payload=json.dumps(data).encode(), content_format=aiocoap.ContentFormat.JSON)


async def main(host, device_id):
    sensor = Sensor(device_id)
    async def update():
        while True:
            sensor.temperature = round(random.uniform(20, 40), 1)
            sensor.humidity = round(random.uniform(30, 90), 1)
            await asyncio.sleep(3)
    site = resource.Site()
    site.add_resource(("iot", "lab", device_id, "data"), sensor)
    await aiocoap.Context.create_server_context(site, bind=(host, 5683))
    print(f"Sensor CoAP Server started: {device_id}", flush=True)
    task = asyncio.create_task(update())
    try:
        await asyncio.get_running_loop().create_future()
    finally:
        task.cancel()


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--device-id", default="sensor01")
    a = p.parse_args()
    try:
        asyncio.run(main(a.host, a.device_id))
    except KeyboardInterrupt:
        print("Server stopped")
