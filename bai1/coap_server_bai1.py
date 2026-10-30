"""May chu CoAP co ban cho bai thuc hanh."""
import argparse
import asyncio
from datetime import datetime

import aiocoap
from aiocoap import resource


class MessageResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.latest = None

    async def render_get(self, request):
        print("GET request received: /iot/lab/message", flush=True)
        return aiocoap.Message(code=aiocoap.Code.CONTENT,
                               payload=(self.latest or "Xin chao tu CoAP Server").encode())

    async def render_post(self, request):
        payload = request.payload.decode("utf-8", errors="replace")
        self.latest = payload
        print("POST request received:", flush=True)
        print(f"Payload: {payload}", flush=True)
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}", flush=True)
        return aiocoap.Message(code=aiocoap.Code.CHANGED, payload=b"Server da nhan thong diep")


async def main(host):
    site = resource.Site()
    site.add_resource(("iot", "lab", "message"), MessageResource())
    await aiocoap.Context.create_server_context(site, bind=(host, 5683))
    print("CoAP Server started on port 5683", flush=True)
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    try:
        asyncio.run(main(args.host))
    except KeyboardInterrupt:
        print("Server stopped", flush=True)
