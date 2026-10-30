"""Bo dieu khien den qua lenh CoAP."""
import argparse
import asyncio
import json

import aiocoap


async def main(host):
    context = await aiocoap.Context.create_client_context()
    uri = f"coap://{host}:5683/iot/lab/light01/status"
    try:
        while True:
            command = (await asyncio.to_thread(input, "Nhap lenh (ON/OFF/STATUS/EXIT): ")).strip().upper()
            if command == "EXIT":
                break
            if command == "STATUS":
                print("Sending GET request...")
                try:
                    response = await context.request(aiocoap.Message(code=aiocoap.Code.GET, uri=uri)).response
                    print("Response:")
                    print(response.payload.decode(errors="replace"))
                except (asyncio.TimeoutError, OSError, aiocoap.error.Error) as exc:
                    print(f"Loi ket noi/timeout CoAP: {exc}")
            elif command in ("ON", "OFF"):
                body = json.dumps({"device_id": "light01", "command": command}).encode()
                print("Sending PUT request...")
                try:
                    response = await context.request(aiocoap.Message(code=aiocoap.Code.PUT, uri=uri, payload=body, content_format=aiocoap.ContentFormat.JSON)).response
                    print(f"Response Code: {response.code}")
                    print(response.payload.decode(errors="replace"))
                except (asyncio.TimeoutError, OSError, aiocoap.error.Error) as exc:
                    print(f"Loi ket noi/timeout CoAP: {exc}")
            else:
                print("Lenh khong hop le. Hay nhap ON, OFF, STATUS hoac EXIT.")
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
    except (KeyboardInterrupt, EOFError):
        print("Da dung controller")
