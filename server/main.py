import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib.util
import os
from pathlib import Path
import sys

# The directory where the bots are located
bots_dir = os.path.join(Path(os.getcwd()).parent, "ai-comedy-club/bots")

# Initialize the FastAPI app
app = FastAPI()
# Initialize the list of bots
bots = []
# Add CORS middleware to allow requests from the frontend
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def load_bots():
    '''
    Load the bots on app startup to avoid loading them on every request and slowing down the server
    '''
    global bots
    sys.setrecursionlimit(20000)
    bot_directories = [d for d in os.listdir(
        bots_dir) if os.path.isdir(os.path.join(bots_dir, d)) and not d.startswith("__")]
    for bot_dir in bot_directories:

        # Dynamically load the bot's module
        spec = importlib.util.spec_from_file_location(
            "bot", os.path.join(bots_dir, bot_dir, "joke_bot.py"))
        bot_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bot_module)

        # Create an instance of the bot and add it to the list
        bot = bot_module.Bot()
        bots.append(bot)
    return ()


async def get_jokes():
    '''
    Get the jokes from every bot and return them in a dictionary of the form {bot_name: joke}
    '''
    jokes_dict = {}
    for bot in bots:
        jokes_dict[bot.name] = bot.tell_joke()
    return jokes_dict


@app.get('/')
async def main():
    jokes_dict = await get_jokes()
    return jokes_dict


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
