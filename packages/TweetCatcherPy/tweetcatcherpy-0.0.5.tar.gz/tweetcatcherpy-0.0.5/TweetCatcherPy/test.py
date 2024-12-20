import asyncio

from TweetCatcherPy import TweetCatcher
from datetime import datetime
import sys


def print(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
    timestamp = f"[{datetime.now()}]"
    output = sep.join(str(arg) for arg in args)
    file.write(f"{timestamp} {output}{end}")
    if flush:
        file.flush()


API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3aG9wVXNlcklkIjoidXNlcl9VTTk3ZzNtTlQ1NXdpIiwidHlwZSI6ImFwaS1rZXkiLCJpYXQiOjE3MzQ2MTY0OTB9.MoI60z6Hb-CcOSQyL3R1BKUAMim6kRBHfmfqtZFqqrM"
tweet_catcher = TweetCatcher(API_TOKEN)


async def run_websocket():
    while True:
        try:
            print("Connecting to WebSocket...")
            await tweet_catcher.start()
            print("Connected to WebSocket.")
            while True:
                message = await tweet_catcher.get_message()
                print("New WebSocket Message:", message)
        except Exception as e:
            print(f"Error: {e}")
            print("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        finally:
            await tweet_catcher.stop()
            print("Disconnected from WebSocket.")


if __name__ == "__main__":
    asyncio.run(run_websocket())
