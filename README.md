# Joke Bot Project

Welcome to the Joke Bot project! This repository contains a Python-based joke bot that generates tailored jokes based on user input and provides a rating for each joke's humor, appropriateness, and more.

## Introduction

The Joke Bot is a fun project that utilizes the GPT-2 language model from the Hugging Face Transformers library to generate jokes based on user preferences. It tailors the jokes according to the user's mood and joke type preference. Additionally, the project includes functionality to rate the generated jokes based on humor, appropriateness, delivery, and awareness of current events or popular culture.

## How It Works

The project consists of two main files:

1. **joke_bot.py**: This file contains the `Bot` class that handles the main functionality of the joke bot. It uses the GPT-2 language model to generate jokes and provides methods for interacting with users and rating jokes.

2. **test_bot.py**: This file contains unit tests for the `Bot` class, ensuring that the core functionality works as expected.

## Joke Generation

The `Bot` class has several methods to facilitate joke generation:

- `ask_user()`: This method prompts the user to provide their mood and joke type preference. It then stores these preferences in the class attributes.

- `tailor_joke()`: This method tailors the beginning of a prompt for the GPT-2 model based on the user's mood and joke type preference. It generates jokes using the tailored prompt and returns the result.

- `tell_joke()`: This method combines the user interaction and joke generation process. It calls `ask_user()` to gather user preferences and then calls `tailor_joke()` to generate and return a joke.

- `rate_joke(joke)`: This method rates a given joke based on various factors:
  - **Humor Rating**: It uses sentiment analysis to determine if the joke is positive and assigns a humor score.
  - **Current Events or Popular Culture Awareness**: It checks for certain terms in the joke and assigns an awareness score.
  - **Content Appropriateness**: It uses content moderation to assess the joke's appropriateness and assigns a score.
  - **Delivery Effectiveness**: It assigns a score based on the joke's length.

## Testing

The `test_bot.py` file contains unit tests for the `Bot` class. It uses the `pytest` framework to ensure that the core functionality of the joke bot works as expected. The tests include:

- Testing the `tell_joke()` method to ensure it generates a joke of appropriate length.
- Testing the `rate_joke()` method to ensure it assigns a valid rating between 1 and 10 based on different factors.



