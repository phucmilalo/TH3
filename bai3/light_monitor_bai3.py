"""Monitor trang thai den bang CoAP Observe that."""
import argparse
import asyncio
import json
from datetime import datetime

import aiocoap


async def main(host):
    context = await aiocoap.Context.create_client_context()
    uri = f"coap://{host}:5683/iot/lab/light01/status"
    try:
        while True:
            observation = None
            try:
                print("Registering CoAP Observe...", flush=True)
                request = context.request(aiocoap.Message(code=aiocoap.Code.GET, observe=0, uri=uri))
                observation = request.observation
                response = await request.response
                print("Observe registration successful", flush=True)
                initial = json.loads(response.payload.decode())
                print(f"[{datetime.now():%H:%M:%S}] Initial State\nDevice: {initial['device_id']}\nStatus: {initial['status']}", flush=True)
                async for update in observation:
                    data = json.loads(update.payload.decode())
                    print(f"[{datetime.now():%H:%M:%S}] State Updated\nDevice: {data['device_id']}\nStatus: {data['status']}", flush=True)
            except asyncio.CancelledError:
                raise
            except (asyncio.TimeoutError, OSError, aiocoap.error.Error, ValueError, KeyError, TypeError) as exc:
                print(f"Observe loi/mat ket noi: {exc}; dang thu dang ky lai", flush=True)
                await asyncio.sleep(2)
            finally:
                if observation is not None and not observation.cancelled:
                    observation.cancel()
    finally:
        await context.shutdown()


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
        print("Da dung monitor")
