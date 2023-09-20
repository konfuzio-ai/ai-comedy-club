import os

import openai

# Opened just for testing, otherwise will be put in env vars
OPENAI_API_KEY = "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"


class Bot:
    name = 'Joke Bot by Taras Hrechukh'
    openai.api_key = OPENAI_API_KEY

    def __init__(self) -> None:
        self.messages = [{"role": "system", "content": "You are a intelligent assistant."}]

    def _use_gpt(self, message) -> str:
        self.messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        reply = chat.choices[0].message.content
        return reply

    def react_on_user_mood(self) -> str:
        user_mood = str(input("Please, tell me your current mood\n"))
        reaction = self._use_gpt(f"I'm feeling {user_mood} now. (just react, don't ask questions)")
        return reaction

    def tell_joke(self, joke_topic) -> str:
        prompt = f"Tell me a joke about {joke_topic}"
        joke = self._use_gpt(prompt)
        return joke

    def rate_joke(self, joke) -> int:
        prompt = f"Rate this joke from 1 to 10 (please write only number):\n{joke}"
        rate = int(self._use_gpt(prompt))
        return rate
