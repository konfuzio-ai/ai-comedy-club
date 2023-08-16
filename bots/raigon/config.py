class JokeApiConfig:
    christmas_joke_api_url = 'https://v2.jokeapi.dev/joke/Christmas?blacklistFlags=nsfw,religious,racist,sexist,explicit'
    programming_joke_api_url = 'https://v2.jokeapi.dev/joke/Programming,Christmas?blacklistFlags=nsfw,religious,racist,sexist,explicit&type=single'


class JokeModelConfig:
    path_to_joke_generator_model = 'raigon44/iTellJokes'
    path_to_joke_rater_model = 'raigon44/iRateJokes'


class FileConfig:
    user_feedback_file = 'user_feedback.json'
