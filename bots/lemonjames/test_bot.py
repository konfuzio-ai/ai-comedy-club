from joke_bot import Bot

def test_instanciate_bot():
    """
    check if class is instantiated
    @return: None
    """
    bot = Bot(False)
    assert not isinstance(bot, type)


def test_tell_joke():
    """
    check function tell_joke()
    @return: None
    """
    bot = Bot(False)
    joke = bot.tell_joke()
    assert isinstance(joke, str)


def test_rate_joke():
    """
    check function rate joke
    @return: None
    """
    bot = Bot(False)
    test_joke = 'Why did the naive Bayesian suddenly feel patriotic when he heard fireworks? He assumed independence.'
    rating = bot.rate_joke(test_joke)
    assert isinstance(rating, int)
    assert 0 <= rating <= 10