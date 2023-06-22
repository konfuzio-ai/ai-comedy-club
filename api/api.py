import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib.util
import os
from pathlib import Path

# This is a simple backend with html template to display ONLY jokes from every bot

# The directory where the bots are located
bots_dir = os.path.join(Path(os.getcwd()).parent, "bots")


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    bots = []
    bot_directories = [d for d in os.listdir(bots_dir) if os.path.isdir(os.path.join(bots_dir, d))]
    for bot_dir in bot_directories:

        # Dynamically load the bot's module
        spec = importlib.util.spec_from_file_location("bot", os.path.join(bots_dir, bot_dir, "joke_bot.py"))
        bot_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bot_module)

        # Create an instance of the bot and add it to the list
        bot = bot_module.Bot()
        bots.append(bot)
    jokes = {}
    for bot in bots:
        jokes[bot.name] = bot.tell_joke()
    return templates.TemplateResponse("index.html", {"request": request, "title": "Comedy-club",
                                                     "placeholder": "Welcome", "jokes": jokes})


if __name__ == "__main__":
    uvicorn.run("api:app", host='127.0.0.1', port=8001, reload=True)

