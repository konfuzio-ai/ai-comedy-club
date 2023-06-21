import pytest
from bots.rosskost.joke_bot import (
    Bot, BOT_NAME, available_jokes, MINUMUM_REASONABLE_JOKE_LENGTH
)
from bots.rosskost.enum_definitions import Topic
from bots.rosskost.save_joke_embeddings import PICKLE_DEST, JOKES_FILE
from bots.rosskost.sbert_space import jokes_from_file
import random
import os

from hypothesis import example, given, settings
from hypothesis.strategies import text


@pytest.fixture
def bot():
    return Bot()

@pytest.fixture
def random_topic():
    return random.choice(list(Topic))


def test_tell_joke(bot):
    joke = bot.tell_joke()
    assert isinstance(joke, str), "Joke is not a string."


def test_rate_joke(bot):
    joke = "Why was the computer cold at the office? Because it left its Windows open."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 1 <= rating <= 10, "Rating is not within the correct range."


def test_rating_int(bot):
    test_joke = "fhdjfghdj"
    rating = bot.rate_joke(test_joke)
    assert isinstance(rating, int)


def test_paths_and_files():
    assert os.path.isfile(PICKLE_DEST), f"pickle file for embeddings in {PICKLE_DEST} is not found."
    assert os.path.isfile(JOKES_FILE), f"File with jokes in {JOKES_FILE} is not found."


@given(text())
@settings(max_examples=50)
def test_rating_hypothesis(test_str: str):
    rating = Bot().rate_joke(test_str)
    assert isinstance(rating, int)

@given(text())
@example("short joke")
def test_short_jokes(joke_str: str):
    bot_instance = Bot()

    if len(joke_str.split()) < MINUMUM_REASONABLE_JOKE_LENGTH:
        assert bot_instance.rate_joke(joke_str) == 1


def test_defaults(bot):
    """Testing the default values of our dataclass Bot"""

    assert bot.name == BOT_NAME
    assert isinstance(bot.name, str)
    assert bot.available_jokes == available_jokes
    assert isinstance(bot.available_jokes, list)
    assert bot.topic is None
    # TODO: ADD rating model once it is added


def test_topic_similarity():
    # we add three of our jokes from the csv file to a short mock joke list and test if the bot tells topic-wise the correct one.
    blondes_jokes: str = "Q: Why do blondes stand under light bulbs? A: It's the closest they'll come to a bright idea."
    sports_joke: str = "What is a horse's favourite sport? Stable tennis!"
    programming_joke: str = "Q: How many programmers does it take to  screw in a light bulb?  A: None that's a hardware problem."
    joke_list = [blondes_jokes, sports_joke, programming_joke]

    bot_instance = Bot(available_jokes=joke_list)

    assert getattr(bot_instance, "available_jokes") == joke_list

    asserted_mapping = {
        sports_joke: Topic.SPORTS,
        blondes_jokes: Topic.BLONDES,
        programming_joke: Topic.PROGRAMMING
    }

    for joke, topic in asserted_mapping.items():
        assert joke == bot_instance.tell_joke(topic=topic, choice_from_top_n=1)

    # if we create a bot-class with a self.topic, choosing another attribute in the tell_joke()-func should overwrite it:
    bot_instance = Bot(topic=topic.SPORTS, available_jokes=joke_list)
    assert programming_joke == bot_instance.tell_joke(topic=Topic.PROGRAMMING, choice_from_top_n=1)

    # w.o. a topic it should choose the self.topic.
    assert sports_joke == bot_instance.tell_joke(choice_from_top_n=1)


def test_behaviour_jokes_w_o_embeddings(random_topic):
    # if we add only one joke, that is not in our csv-file and hence has no embedding,
    # we should only be able to tell that joke without a topic:
    some_joke = ["Why was the computer cold at the office? Because it left its Windows open."]

    # check that this joke is not already there:
    assert some_joke not in [joke for _, joke in jokes_from_file]

    bot_instance = Bot(available_jokes=[some_joke])
    # only one joke in list, so we should tell it on asking:
    assert some_joke == bot_instance.tell_joke()

    # only one unembedded joke and asking for any topic should throw an error:
    with pytest.raises(ValueError):
        bot_instance.tell_joke(topic=random_topic)

    # we should be able to add jokes after bot instance is created (per default with all abailable jokes):
    bot_instance = Bot()
    bot_instance.available_jokes.append(some_joke)

    assert some_joke in bot_instance.available_jokes


def test_too_many_similar_jokes(bot, random_topic):
    with pytest.raises(ValueError):
        bot.tell_joke(topic=random_topic, choice_from_top_n=10**10)

    # without a topic, we should not care about that parameter and just return a random joke, without any errors:
    assert isinstance(bot.tell_joke(choice_from_top_n=10**10), str)
