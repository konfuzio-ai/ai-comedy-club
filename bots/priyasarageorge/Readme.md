
# Joke Bot

Joke Bot is a Python-based chatbot that can tell jokes, rate jokes, and provide a fun and interactive experience for users.

## Project Overview

The Joke Bot project is designed to entertain users with jokes and humor. It leverages natural language processing techniques and machine learning to provide a personalized joke-telling experience. Users can interact with the bot by asking for jokes, rating jokes, and receiving jokes from different categories, such as happy, sad, or neutral.

## Dataset

The Joke Bot project uses the "Jester Dataset 1" for training and generating jokes. This dataset consists of user ratings for various jokes, along with the text of the jokes themselves. The dataset is utilized for training a machine learning model to predict joke ratings based on sentiment analysis and joke length.

- **Dataset Name**: Jester Dataset 1
- **Dataset Source**: [Jester Dataset 1](http://eigentaste.berkeley.edu/dataset/)
- **Dataset Description**: The dataset contains user ratings for jokes on a scale from -10 to 10, where -10 represents the least funny and 10 represents the funniest. Additionally, it includes the text of the jokes.

## Project Components

The Joke Bot project consists of the following components:

1. **Bot Class (joke_bot_1.py):** The core logic of the chatbot, including joke retrieval, rating, and training of the joke rating prediction model.

2. **TestBot Class (test_bot.py):** A unit testing suite to verify the functionality of the Bot class methods.

3. **Linear Regression Model (linear_regression_model_polarity_length.pkl):** A trained machine learning model for predicting joke ratings based on polarity and joke length.

## Dependencies

Make sure to install the required Python libraries and packages before running the Joke Bot:

- transformers
- scikit-learn
- pandas
- textblob
- bs4

You can install these dependencies using `pip` or another package manager.

- pip install transformers
- pip install scikit-learn
- pip install pandas
- pip install textblob
- pip install bs4
- pip install torchvision --user
- pip install xlrd

## Usage

To run the Joke Bot, execute the `joke_bot_1.py` script in your Python environment:

```bash
python joke_bot_1.py
```

The bot will interact with you, allowing you to request jokes, rate jokes, and enjoy a humorous experience.

## Testing

To ensure the correctness of the bot's functionality, you can run the unit tests provided in the `test_bot.py` script:

```bash
python test_bot.py
```

The tests will validate the core features of the Joke Bot, including joke retrieval, sorting, model training, and joke rating.

Happy joking!
```

