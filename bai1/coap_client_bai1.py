"""Client CoAP co ban: GET, POST lap va thu URI loi."""
import argparse
import asyncio

import aiocoap


async def main(host, student_id, name, count, test_missing):
    context = await aiocoap.Context.create_client_context()
    uri = f"coap://{host}:5683/iot/lab/message"
    try:
        print("Sending GET request...")
        print(f"URI: {uri}")
        response = await context.request(aiocoap.Message(code=aiocoap.Code.GET, uri=uri)).response
        print("Response:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode(errors='replace')}")
        for _ in range(count):
            payload = f"Xin chao tu CoAP Client - {student_id} - {name}"
            print("Sending POST request...")
            print(f"Payload: {payload}")
            response = await context.request(aiocoap.Message(code=aiocoap.Code.POST, uri=uri, payload=payload.encode())).response
            print("Response:")
            print(f"Code: {response.code}")
            print(f"Payload: {response.payload.decode(errors='replace')}")
        if test_missing:
            bad = f"coap://{host}:5683/iot/lab/missing"
            response = await context.request(aiocoap.Message(code=aiocoap.Code.GET, uri=bad)).response
            print(f"Missing URI Code: {response.code}")
    except (asyncio.TimeoutError, OSError, aiocoap.error.Error) as exc:
        print(f"Loi ket noi/timeout CoAP: {exc}")
    finally:
        await context.shutdown()


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--student-id", default="B23DCCN957")
    p.add_argument("--name", default="Nguyen Van Phuc")
    p.add_argument("--count", type=int, default=1)
    p.add_argument("--test-missing", action="store_true")
    a = p.parse_args()
    try:
        asyncio.run(main(a.host, a.student_id, a.name, max(1, a.count), a.test_missing))
    except KeyboardInterrupt:
        print("Da dung client")
