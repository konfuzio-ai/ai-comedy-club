# The Comedy King

The Comedy King is a bot that can both generate and rate jokes. It employs advanced machine learning models and techniques to achieve these tasks.

## Features

- **Joke Generation:** For joke generation, the bot uses a fine-tuned gpt2-medium model. The GPT-2 model is a transformer-based language model developed by OpenAI and is known for its impressive text generation capabilities. The model was fine-tuned on a dataset of short jokes and uses the tokens `<|im_start|>` and `<|end|>` to mark the beginning and end of a joke. The bot employs an exploration strategy for the next word prediction, where it chooses from the top n most probable tokens, adding a degree of randomness and creativity to the generated jokes.

- **Joke Rating:** For joke rating, the bot uses a combination of BERT embeddings, TextBlob sentiment signals, and an XGBoost classifier. The prajjwal1/bert-tiny model is used to generate embeddings for the input text, which are high-dimensional vector representations that capture the semantic content of the text. TextBlob is used to compute the polarity and subjectivity of the text, providing an indication of the sentiment of the joke. These features are then fed into an XGBoost classifier, a powerful gradient-boosting framework, to predict a rating between 0 and 10 for the joke. The data used is the Reddit joke scores where a logarithmic transformation was applied to the scores which were then normalized. The same distribution of jokes was taken for each category to counter the imbalance.

## Installation

To install the necessary libraries, run the following command:

```bash
pip install tensorflow transformers xgboost textblob pandas
```
## Training

The training was done on Google Colab because of the availability of more resources. The detail can be seen in the ***training*** directory.

## Weights

The weights for both the XGBoost and GPT2 models are stored in the Weights folder. Due to Git LFS limitations towards public forked repositories, the ckpt-3.data-00000-of-00001 file needs to be downloaded separately from this [Google Drive link](https://drive.google.com/file/d/1-Yv0rq_wYrEYJ_g_TxAFEbAHYkW9egxw/view?usp=drive_link).

After downloading, place the ckpt-3.data-00000-of-00001 file into the Weights/GPT2_Medium directory. The file size is 1.3 GB.

## Usage

First, import the Bot class from bot.py:

```python
from bot import Bot
```

Then, you can create a new instance of the bot:

```python
bot = Bot()
```

To generate a joke, use the `tell_joke` method:

```python
joke = bot.tell_joke()
print(joke)
```

To rate a joke, use the `rate_joke` method:

```python
rating = bot.rate_joke("Why don't scientists trust atoms? Because they make up everything!")
print(rating)
```

## Examples

Example outputs and usage can be seen in `Output Examples.ipynb`. Following are some examples:

### Joke Generation

Here are some examples of jokes generated by the bot:

- "When is an argument never an argument? When there are no arguments."
- "Did you hear about the man who got a new job as a plumber? He was a new hire. He was a little bit rusty."
- "What's a pirates favorite letter? Aye! I'll show myself out."
- "What do you call a Mexican that can only count to three? Juan Juan Juan Juan."
- "I can't believe the guy who invented the vacuum is still alive."

The model is capable of generating jokes with good humor and creativity. It can even generate jokes with a hint of sarcasm and dark humor. The start and end tokens also seem to work well, allowing the model to correctly identify the end of a joke. For example Joke 4. The model knows the stereotype regarding all Mexicans named Juan and witty humor for the only known word being Juan where the fourth Juan is the name. The model has learned well where to stop.

### Joke Rating

Here are some examples of joke ratings:

- "Why don't scientists trust atoms? Because they make up everything!" - Rating: 6.0
- "What do you call a bear with no teeth? A gummy bear!" - Rating: 2.0

### Testing Bot

Test cases have been created using `pytest` in the ***test_bot.py***.

### Future Improvements

I would want to move toward the latest LLMs for this task. I have tested some prompts in GPT4 and it works very well. Did not include in this implementation because of service charges. Prompt engineering can be used to generate specific jokes/ rate specific aspects of jokes. If we want to finetune, we can try bigger LLMs like `Llama 2` and `Falcon` on our data. But it would require a lot of resources.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
