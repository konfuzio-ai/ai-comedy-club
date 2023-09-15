"""
This Python code defines a class called Bot that can tell jokes and rate jokes.

The Bot class has two methods:

* tell_joke(msg: str = "Make me laugh.") -> str: This method tells a joke. The default message is "Make me laugh."
* rate_joke(joke: str) -> int: This method rates a joke on a scale of 1 to 10.

The Bot class uses the OpenAI API to generate jokes and ratings.
"""
from os import getenv

import openai

openai.api_key = getenv("OPENAI_API_KEY")


class Bot:
    """
    A human-like comedian who tells jokes and review other people's jokes, but not their own.
    """
    def tell_joke(self, msg: str = "Make me laugh.") -> str:
        """Tells a joke. The default message is "Make me laugh."

        :param msg: The message to be used as the prompt for the joke.
        :type msg: str
        :return: The generated joke.
        :rtype: str
        """
        response =  openai.ChatCompletion.create(
            model=getenv("OPENAI_MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": "A human-like comedian who tells jokes and review other people's jokes, but not their own."
                },
                {
                    "role": "user",
                    "content": msg
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )["choices"][0]["message"]["content"]
        return response

    def rate_joke(self, joke: str) -> float:
        """
        Rates a joke on a scale of 1 to 10.

        :param joke: The joke to be rated.
        :type: str
        :return: The rating of the joke.
        :rtype: str
        """
        response =  openai.ChatCompletion.create(
            model=getenv("OPENAI_MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": "Comedy judge who rates jokes on a scale of 1 to 10, gives only a number."
                },
                {
                    "role": "user",
                    "content": joke
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )["choices"][0]["message"]["content"]
        return float(response)
    