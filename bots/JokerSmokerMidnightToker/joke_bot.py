import json
import random
from agents.joke_rating_agent import joke_rating_agent_executor
from agents.joke_telling_agent import joke_telling_agent_executor

class Bot:
    def tell_joke(self, joke_instruction):
        reply = joke_telling_agent_executor.run(joke_instruction)
        return reply

    def rate_joke(self, joke):
        resp = joke_rating_agent_executor.run(joke)
        json_resp = json.loads(resp.replace("\'", "\""))
        return int(json_resp['rating'])

    def verify_context(self, context, llm_reply):
        # Here we would check the context/inference, by adding a new agent that checks the context/inference: joke_verify_context_agent.py
        # Example prompt: Check if joke: {llm_reply} is about: {context} // "birds and trees". Output should be in json: { context: Boolean(value) }
        return True
