# Funnybot

This bot's name is taken from the [South Park character](https://southpark.fandom.com/wiki/Funnybot_(Character)),
however, we've put some effort to prevent it from using any foul language.

This project uses machine learning, i.e., [GPT2 transformers](https://huggingface.co/docs/transformers/model_doc/gpt2) from [Hugging Face](https://huggingface.co/) to generate and classify text.

For more details on how the transformers were created, refer to the [jupyter notebooks](./transformers/notebooks).

## Dependencies

Install comedy club's dependencies (minimal depencies for execution):

```
pip install .
```

Install this project's dependencies (only required for training/generating the transformers and automated tests):

```
pip install -r bots/funnybot/requirements-dev.txt
```

## Running tests

```
pytest bots/funnybot -s -v
```

You should get something like the following output:

```
pytest -s -v 
================ test session starts ===========================================================================================
platform linux -- Python 3.10.9, pytest-7.4.0, pluggy-1.2.0 -- /home/marcio/workspace/konfuzio-ai/ai-comedy-club/bots/funnybot/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/marcio/workspace/konfuzio-ai/ai-comedy-club
plugins: anyio-3.7.1
collected 4 items                                                                                                                                                                                         

test_bot.py::BotTest::test_rates_joke PASSED
test_bot.py::BotTest::test_tells_joke_to_a_bit_fussy_user PASSED
test_bot.py::BotTest::test_tells_joke_to_a_easy_going_user PASSED
test_bot.py::BotTest::test_tells_joke_to_a_fussy_user PASSED

================ 4 passed in 14.12s ============================================================================================
```

## Development

The models used in this project have been uploaded to Hugging Face's Hub. Right out of the box, you may run the application (for real or unit tests) using these public models, which will be downloaded from the Hub.

However, for development purposes, makes more sense to load the models from our local development environment. To do that, you are required to set the following environment variable:

```
export IS_LOCAL=true
```

Once you do that, the models will be loaded from the local disk, so be sure to build and save the models by running the Jupyter notebooks.

## Getting on Stage

```
python main.py
```