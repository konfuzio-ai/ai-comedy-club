import pyjokes
import random

CUSTOM_LANGUAGE = 'en'
PYJOKES_CATEGORIES = ['neutral', 'chuck', 'all']
CUSTOM_CATRGORIES = ['programmer', 'computer', 'error', 'Java']

def get_categories():
    """
    This function returns the categoris defined in our custom pyjokes.

    Returns
    -------
    List of strings
        The categories defined in this module.

    """
    return PYJOKES_CATEGORIES + CUSTOM_CATRGORIES

def get_joke(joke_bot, category='neutral'):
    """
    This function generates jokes based on the pyjokes.

    Parameters
    ----------
    joke_bot : Bot
        The bot used to rate the joke.
    category : string, optional
        The category states the category, from which the joke shall be taken.
        The default is 'neutral'.

    Raises
    ------
    Exception
        The exception is raised in case an invalid category was given.

    Returns
    -------
    string
        The generated jokes.

    """
    if category in PYJOKES_CATEGORIES:
        jokes = pyjokes.get_jokes(CUSTOM_LANGUAGE, category)
        if (jokes == []):
            jokes = pyjokes.get_jokes(CUSTOM_LANGUAGE, category='all')
    elif category in CUSTOM_CATRGORIES:
        jokes = pyjokes.get_jokes(CUSTOM_LANGUAGE, category='all')
        jokes = [i for i in jokes if category in i]
    else:
        raise Exception("Invalid category: " + str(category))
    jokes_ratings = [joke_bot.rate_joke(i) for i in jokes]
    return random.choices(jokes, weights=jokes_ratings)[0]