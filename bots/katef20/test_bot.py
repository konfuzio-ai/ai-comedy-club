from joke_bot import Bot


def test_tell_joke():
    jokebot = Bot()
    joke = jokebot.tell_joke()

    assert jokebot.prefix in joke
    assert jokebot.who in joke
    assert jokebot.someone_who() in joke
    assert jokebot.joke_ending() in joke


def test_rate_joke():
    jokebot = Bot()
    joke = jokebot.tell_joke()
    rating = jokebot.rate_joke(joke)

    assert 'Polarity' in rating
    assert 'Subjectivity' in rating
    assert 'Assessments' in rating

    assert -1 < rating['Polarity'] < 1
    assert -1 < rating['Subjectivity'] < 1
    assert type(rating['Assessments']) == list


def test_someone_who():
    jokebot = Bot()
    ending = jokebot.someone_who()

    assert jokebot.who in ending
    assert ending.endswith('who?')


def test_joke_ending():
    jokebot = Bot()
    ending = jokebot.joke_ending()

    assert ending in jokebot.endings
    assert ending.startswith(jokebot.who.title())
