from joke_bot import Bot

def test_tell_joke():
    bot = Bot()
    joke = bot.tell_joke()
    assert isinstance(joke, str)

def test_rate_joke():
    bot = Bot()

    # Test a mildly funny joke
    joke1 = "There are 10 types of people in the world. Those who understand binary and those who don't."
    user_preferences1 = ["puns"]
    assert bot.rate_joke(joke1, user_preferences1) >= 5  # Should be rated as funny

    # Test a creative joke
    joke2 = "Why did the AI go to therapy? It had too many neural issues."
    user_preferences2 = ["creative"]
    assert bot.rate_joke(joke2, user_preferences2) >= 5  # Should be rated as funny

    # Test a personalized joke (matching user preference)
    joke3 = "Why did the AI go to therapy? It had too many neural issues."
    user_preferences3 = ["neural issues"]
    assert bot.rate_joke(joke3, user_preferences3) >= 5  # Should be rated as funny

    # Test a joke below the humor threshold
    joke4 = "Why did the AI go to the store? To buy some bytes."
    assert bot.rate_joke(joke4) == 1  # Should be rated as not funny

    # Test a joke that lacks personalization
    joke5 = "Why are humans known to be extremely afraid of computers? Probably, because they byte."
    user_preferences5 = ["puns"]
    assert bot.rate_joke(joke5, user_preferences5) <= 5  # Should not be highly rated
