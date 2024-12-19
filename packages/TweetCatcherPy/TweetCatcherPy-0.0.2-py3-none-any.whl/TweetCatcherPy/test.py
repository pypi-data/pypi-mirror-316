import asyncio

from main import TweetCatcher

API_TOKEN = "..-ot8"
tweet_catcher = TweetCatcher(API_TOKEN)


async def run_websocket():
    while True:
        try:
            await tweet_catcher.start()
            print("Connected to WebSocket.")
            while True:
                message = await tweet_catcher.get_message()
                print("New WebSocket Message:", message)
        except Exception as e:
            print(f"Error: {e}")
            print("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(run_websocket())
