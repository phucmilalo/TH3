"""May chu den thong minh co ho tro CoAP Observe."""
import argparse
import asyncio
import json

import aiocoap
from aiocoap import resource


class Light(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.status = "OFF"

    def update_observation_count(self, newcount):
        if newcount:
            print("New Observe registration received", flush=True)

    def payload(self):
        return json.dumps({"device_id": "light01", "status": self.status}).encode()

    async def render_get(self, request):
        return aiocoap.Message(code=aiocoap.Code.CONTENT, payload=self.payload(), content_format=aiocoap.ContentFormat.JSON)

    async def render_put(self, request):
        print("PUT request received:", flush=True)
        try:
            data = json.loads(request.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return aiocoap.Message(code=aiocoap.Code.BAD_REQUEST, payload=b"Payload khong phai JSON hop le")
        if not isinstance(data, dict) or "device_id" not in data or "command" not in data:
            return aiocoap.Message(code=aiocoap.Code.BAD_REQUEST, payload=b"Thieu truong device_id hoac command")
        if data["device_id"] != "light01":
            return aiocoap.Message(code=aiocoap.Code.BAD_REQUEST, payload=b"device_id khong hop le")
        command = data["command"]
        print("Device: light01", flush=True)
        print(f"Command: {command}", flush=True)
        if command not in ("ON", "OFF"):
            return aiocoap.Message(code=aiocoap.Code.BAD_REQUEST, payload=b"command phai la ON hoac OFF")
        previous = self.status
        if command != previous:
            self.status = command
            print(f"Light state changed: {previous} -> {self.status}", flush=True)
            self.updated_state()
            print(f"Notify observers: {self.status}", flush=True)
        confirmation = "Da bat den light01" if command == "ON" else "Da tat den light01"
        return aiocoap.Message(code=aiocoap.Code.CHANGED, payload=confirmation.encode())


async def main(host):
    light = Light()
    site = resource.Site()
    site.add_resource(("iot", "lab", "light01", "status"), light)
    await aiocoap.Context.create_server_context(site, bind=(host, 5683))
    print("CoAP Smart Light Server started...", flush=True)
    print("Resource: /iot/lab/light01/status", flush=True)
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    a = p.parse_args()
    try:
        asyncio.run(main(a.host))
    except KeyboardInterrupt:
        print("Server stopped")
