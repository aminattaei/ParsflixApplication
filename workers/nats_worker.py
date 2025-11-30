import asyncio
from nats.aio.client import Client as NATS
from nats.js.client import JetStreamContext

async def run():
    nc = NATS()
    await nc.connect("nats://localhost:4222")
    js = JetStreamContext(nc)

    async def message_handler(msg):
        data = msg.data.decode()
        print("Received event:", data)
        await msg.ack()

    # Subscribe with callback
    await js.subscribe("user.registered", cb=message_handler)

    print("worker is listening forever...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
