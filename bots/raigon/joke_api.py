import requests


def get_joke(api_url):
    response = requests.get(api_url).json()
    if response['type'] == 'twopart':
        return response['setup']+' '+response['delivery']
    else:
        return response['joke']


if __name__ == '__main__':
    joke = get_joke('https://v2.jokeapi.dev/joke/Christmas?blacklistFlags=nsfw,religious,racist,sexist,explicit')
    print(joke)
