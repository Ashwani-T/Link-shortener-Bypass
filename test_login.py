from user_client import client

async def main():
    await client.start()
    print("Logged in successfully")

with client:
    client.loop.run_until_complete(main())
