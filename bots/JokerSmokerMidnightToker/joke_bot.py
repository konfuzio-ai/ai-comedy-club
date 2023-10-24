import json
import random
import sys
import os
import random

from bots.JokerSmokerMidnightToker.agents.joke_rating_agent import joke_rating_agent_executor
from bots.JokerSmokerMidnightToker.agents.joke_telling_agent import joke_telling_agent_executor

predefined_jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the chicken go to the seance? To talk to the other side.",
            "Why don't some animals play cards? Because they're afraid of cheetahs.",
            "What do you call fake spaghetti? An impasta!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]

class Bot:
    name = "JokerSmokerMidnightToker"

    def tell_joke(self, joke_instruction=random.choice(predefined_jokes)):
        reply = joke_telling_agent_executor.run(joke_instruction)
        return reply

    def rate_joke(self, joke):
        resp = joke_rating_agent_executor.run(joke)
        json_resp = json.loads(resp.replace("\'", "\""))
        return int(json_resp['rating'])

    def verify_context(self, context, llm_reply):
        # Here we would check the context vs the llm_reply, by adding a new agent: joke_verify_context_agent.py
        # Example prompt: Check if joke: {llm_reply} is about: {context} // "birds and trees". Output should be in json: { context: Boolean(value) }
        return True
