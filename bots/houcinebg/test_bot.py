import pytest
from joke_bot import Bot

# Fixture to initialize the Bot instance
@pytest.fixture
def bot():
    return Bot(r'D:\Konfuzio\ai-comedy-club\bots\houcinebg\cleanjokes.csv',"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")  # Path to Jokes dataset csv file 

# Test for checking the name of the bot
def test_bot_name(bot):
    jokes_file = r'D:\Konfuzio\ai-comedy-club\bots\houcinebg\cleanjokes.csv'
    gpt_api_key = "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"

    bot = Bot(jokes_file,gpt_api_key)
    assert bot.name == "HaHa_Too_Funny_Bot"

# Test for checking the format of the jokes in the dataset
def test_joke_file_format(bot):
    joke = bot.tell_joke()
    assert isinstance(joke, str)

# Test for checking the encoding of jokes in the dataset
def test_joke_file_encoding(bot):
    joke = bot.tell_joke()
    assert isinstance(joke, str)
    assert joke.encode("utf-8").decode("utf-8") == joke  # Ensure the joke can be encoded and decoded using UTF-8

# Test for checking the rating score of a joke
def test_rate_joke_score(bot):
    joke = bot.tell_joke()
    rating = bot.rate_joke(joke)
    assert isinstance(rating, int)
    assert rating >= 0 and rating <= 10

# Run all the tests
if __name__ == "__main__":
    pytest.main()
