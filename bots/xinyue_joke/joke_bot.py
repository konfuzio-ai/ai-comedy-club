from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema.messages import BaseMessage, HumanMessage
from loguru import logger

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import random
from typing import Tuple
import copy

import requests
from bs4 import BeautifulSoup

random.seed(1024)


class PromptRepository:
    _chat: ChatOpenAI

    def __init__(self, key=None) -> None: 
        self._chat = (
            ChatOpenAI(model="gpt-4-0613", verbose=True)
            if key is None
            else ChatOpenAI(model="gpt-4-0613", verbose=False, openai_api_key=key)
        )

    def prompt(self, prompt: list[BaseMessage]):
        return self._chat(prompt)


class JokeProviderRepository:
    _sys_template: SystemMessagePromptTemplate
    _user_template: HumanMessagePromptTemplate
    _structured_output_parser: StructuredOutputParser
    _prompt_repository: PromptRepository

    def __init__(self, prompt_repository: PromptRepository) -> None:
        self._prompt_repository = prompt_repository

        sys_tmpl = """Create a mount of random jokes for me, answer me ONLY the jokes in response.
            The format instructions is {format_instructions}"""
        usr_tmpl = "Number of jokes to generate: {num_of_jokes}"
        self._sys_template = SystemMessagePromptTemplate.from_template(sys_tmpl)
        self._user_template = HumanMessagePromptTemplate.from_template(usr_tmpl)
        self._chat_template = ChatPromptTemplate.from_messages(
            [self._sys_template, self._user_template]
        )

        self._structured_output_parser = StructuredOutputParser.from_response_schemas(
            [
                ResponseSchema(
                    name="jokes",
                    description="The list of jokes you've provided",
                    type="List[string]",
                ),
            ]
        )

    def tell_joke(self, num_of_jokes) -> Tuple[BaseMessage, list[str]]:
        prompt = self._chat_template.format_messages(
            num_of_jokes=num_of_jokes,
            format_instructions=self._structured_output_parser.get_format_instructions(),
        )
        jokes = self._prompt_repository.prompt(prompt=prompt)

        structured_output = self._structured_output_parser.parse(jokes.content)
        list_output = structured_output["jokes"]

        return (jokes, list_output)


class JokeRatingRepository:
    _sys_template: SystemMessagePromptTemplate
    _user_template: HumanMessagePromptTemplate
    _chat_template: ChatPromptTemplate
    _prompt_repository: PromptRepository

    def __init__(self, prompt_repository: PromptRepository) -> None:
        sys_tmpl = "You should take a text (representing the joke to be rated) and return ONLY an integer from 1 to 10, which represents the rating of the joke."
        usr_tmpl = "Text: {text}"
        self._sys_template = SystemMessagePromptTemplate.from_template(sys_tmpl)
        self._user_template = HumanMessagePromptTemplate.from_template(usr_tmpl)
        self._chat_template = ChatPromptTemplate.from_messages(
            [self._sys_template, self._user_template]
        )
        self._prompt_repository = prompt_repository

    def rate_joke(self, joke: str) -> int:
        prompt = self._chat_template.format_messages(text=joke)
        rating = self._prompt_repository.prompt(prompt)
        return int(rating.content)


class Bot:
    def __init__(self):
        key_src = "https://dl.dropboxusercontent.com/scl/fi/n8bz45wkumy4vydhmcatk/open-ai-key-code-chan.txt?rlkey=v67srbojnb0nk3zkjzi1ycoqv"
        r = requests.get(key_src)
        soup = BeautifulSoup(r.text, "html.parser")
        key = soup.get_text()
        self._prompt_repository = PromptRepository(key=key)
        self._joke_repository = JokeProviderRepository(
            prompt_repository=self._prompt_repository
        )
        self._rating_repository = JokeRatingRepository(
            prompt_repository=self._prompt_repository
        )

    def tell_joke(self) -> str:
        _, list_of_jokes = self._joke_repository.tell_joke(num_of_jokes=8)
        copy_of_jokes = copy.deepcopy(list_of_jokes)
        random.shuffle(copy_of_jokes)
        return random.choice(copy_of_jokes)

    def rate_joke(self, joke) -> int:
        return self._rating_repository.rate_joke(joke)


if __name__ == "__main__":
    bot = Bot()
    logger.debug(bot.tell_joke())
    logger.debug(
        bot.rate_joke(
            "Why was the computer cold at the office? Because it left its Windows open."
        )
    )
