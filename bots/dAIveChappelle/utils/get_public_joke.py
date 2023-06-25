from typing import Optional
import requests


def get_public_joke(config: dict) -> Optional[str]:
    '''
    This function gets a joke from one of the public APIS provided in the config file ./config/basemodel.py
    '''
    try:
        joke = requests.get(
            config.JOKE_API_ENDPOINTS[1]).json()
        if joke['type'] == 'single':
            joke = joke['joke']
        else:
            joke = joke['setup'] + '\n' + joke['delivery']
    except:
        joke = requests.get(
            config.JOKE_API_ENDPOINTS[0]).json()
        joke = joke['setup'] + '\n' + joke['punchline']

    return (joke)
