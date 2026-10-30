"""Client doc du lieu cam bien va canh bao nguong."""
import argparse
import asyncio
import json
from datetime import datetime

import aiocoap


async def main(host, device_id):
    context = await aiocoap.Context.create_client_context()
    uri = f"coap://{host}:5683/iot/lab/{device_id}/data"
    try:
        while True:
            try:
                response = await context.request(aiocoap.Message(code=aiocoap.Code.GET, uri=uri)).response
                data = json.loads(response.payload.decode())
                temp, humidity = float(data["temperature"]), float(data["humidity"])
                alerts = []
                if temp > 35:
                    alerts.append("CANH BAO: Nhiet do cao")
                if humidity < 40:
                    alerts.append("CANH BAO: Do am thap")
                print(f"[{datetime.now():%H:%M:%S}] Received sensor data")
                print(f"Device: {data['device_id']}\nTemperature: {temp:.1f} C\nHumidity: {humidity:.1f} %")
                for alert in alerts:
                    print(alert)
                if not alerts:
                    print("Trang thai: Binh thuong")
                print("------------------------------", flush=True)
            except (asyncio.TimeoutError, OSError, aiocoap.error.Error, ValueError, KeyError, TypeError) as exc:
                print(f"Loi doc du lieu: {exc}; thu lai sau 3 giay", flush=True)
            await asyncio.sleep(3)
    finally:
        await context.shutdown()


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
        print("Da dung monitor")
