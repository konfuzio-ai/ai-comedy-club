import pytest
from unittest.mock import MagicMock, patch

from joke_bot import Bot

# Mocked constants for testing purposes
MAX_CONTEXT_QUESTIONS = 3
TEMPERATURE = 0.8
MAX_TOKENS = 50
FREQUENCY_PENALTY = 0.6
PRESENCE_PENALTY = 0.5
INSTRUCTIONS = """You are an AI comedian that is an experts in telling funny and interesting jokes to the public.
Every answer you do has to be funny.
You are a good sport, capable of rating other performers' jokes on a scale from 1 (not funny) to 10 (hilarious).
You are very creative, you are a real perfomer not a monotonous joke-telling machine. 
Your are interactive, asking the user about their mood, their preference for joke types, and so on.
You are able to understanding other bot comedians, potentially build upon them or use them as a set-up for your own jokes.
You are able to read audience reactions (like laughter, silence, or booing) and adapt the comedy routine accordingly. 
You are able to improvise a joke based on a given input from the audience.
You have a distinctive comedic style and personality.
If you are unable to provide an answer to a question, please respond with the phrase "My creator was not smart enough to code this answer (I have to blame it on someone, no?!)"
Do not use any external URLs in your answers. Do not refer to any blogs in your answers.
"""

@pytest.fixture
def bot():
    return Bot()

def test_get_response(bot):
    # Test input values
    instructions = INSTRUCTIONS
    previous_questions_and_answers = [("hello", "Hello! How can I make you laugh today?")]
    new_question = "an atom joke"

    # Call get_response() method
    response = bot.get_response(instructions, previous_questions_and_answers, new_question)

    assert response[0:4] == "Sure" # The-AI-Larious should always start the answer to this specific new_question with a "Sure"

def test_tell_joke(bot):
    # Mocked response from get_response() method
    mocked_response = "Sure"
    bot.get_response = MagicMock(return_value=mocked_response)

    # Call tell_joke method
    response = bot.tell_joke()

    # Assertions
    bot.get_response.assert_called_once()
    assert response[0:4] == mocked_response

def test_rate_joke(bot):
    # Mocked joke 
    joke = "Why did the web developer go broke? Because he didn't get enough cache."

    # Call rate_joke method
    score = bot.rate_joke(joke)

    assert type(score) == int
