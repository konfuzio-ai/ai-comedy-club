from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class dAIveConfig(BaseModel):
    '''Config class for the variables used by dAIve Chapelle.'''
    OPEN_AI_API_KEY: str = os.environ.get('OPENAI_API_KEY')
    MODEL_CONTEXT: str = "The following is a conversation with an AI assistant. The assistant is called dAIve Chappelle a funny, hilarious ai comedian and always says creative jokes. The assistant should only answer with the joke without prefixes.\n\n"
    MODEL_ID: str = "text-davinci-003"
    MODEL_PARAMS: dict = {"temperature": 1, "max_tokens": 250, "top_p": 0.75,
                          "frequency_penalty": 0, "presence_penalty": 0.6, "stop": [" Human:", " AI:"]}
    JOKE_API_ENDPOINTS: list = ["https://official-joke-api.appspot.com/random_joke",
                                "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,racist,sexist,explicit"]
