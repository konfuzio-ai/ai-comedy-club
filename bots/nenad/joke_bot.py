!pip install transformers

import logging
logging.getLogger().setLevel(logging.CRITICAL)

import torch
import numpy as np

from transformers import GPT2Tokenizer, GPT2LMHeadModel


from transformers import pipeline
from textblob import TextBlob
import random

class Bot:
  name = 'Try AI to funny'
  def __init__(self):
    """
    self.joke_generator = pipeline('text-generation', model='gpt2')
    self.joke_prefixes = [
      "My best joke is: "
    ]
    """
    self.device = 'cpu'
    if torch.cuda.is_available():
      self.device = 'cuda'

    self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    self.model = GPT2LMHeadModel.from_pretrained('gpt2')
    self.model = self.model.to(self.device)

    """
    def tell_joke(self):
        # Use the GPT-2 model to generate a joke
        # Choose a random prefix for the joke
        prefix = random.choice(self.joke_prefixes)
        joke = self.joke_generator(f'{prefix}', max_length=25, do_sample=True)[0]['generated_text']
        return joke
    """
    """
    def rate_joke(self, joke):
        # Rate the joke based on its sentiment polarity
        # This is a simple example and doesn't actually reflect humor
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        rating = (polarity + 1) * 5  # convert polarity from [-1, 1] to [0, 10]
        return rating
    """

  #Checks if any comibnation of tokens which make the forbidden word are present in the new sequence after adding token
  def check_forbidden(self, f_sequence, current_sequence):
      if (current_sequence.find(f_sequence)==-1):
        return False
      else:
        return True

  #Loads a list of forbidden words from file and finds their token combinations from vocabulary
  def get_forbidden_token_list(self, tokenizer, bad_words, min_strlen=2):
      vocab_tokens = self.tokenizer.get_vocab()
      vocab = {}

      for token in vocab_tokens:
          vocab[tokenizer.convert_tokens_to_string([token])] = token

      results = []

      for bad_word in bad_words:
          confirmed_tokens = []
          possible_tokens = []
          for token in vocab:
              if bad_word == token:
                  confirmed_tokens.append([token])
              elif bad_word.startswith(token):
                  possible_tokens.append([token])
          while len(possible_tokens) > 0:
              new_possible_tokens = []
              for prefixes in possible_tokens:
                  prefix = ''.join(prefixes)
                  for token in vocab:
                      if len(token) < min_strlen:
                          continue
                      if bad_word == prefix + token:
                          found_prefix = prefixes.copy()
                          found_prefix.append(token)
                          confirmed_tokens.append(found_prefix)
                      elif bad_word.startswith(prefix + token):
                          found_prefix = prefixes.copy()
                          found_prefix.append(token)
                          new_possible_tokens.append(found_prefix)
              possible_tokens = new_possible_tokens
          results += confirmed_tokens

      ids = []
      for tokens in results:
          gtokens = []
          for token in tokens:
              gtokens.append(vocab[token])
          ids.append(tokenizer.convert_tokens_to_ids(gtokens))
      return ids


  # Function to first select topN tokens from the probability list and then based on the selected N word distribution
  # get random token ID
  def choose_from_top(self, probs, n=5):
      ind = np.argpartition(probs, -n)[-n:]
      top_prob = probs[ind]
      top_prob = top_prob / np.sum(top_prob) # Normalize
      choice = np.random.choice(n, 1, p = top_prob)
      token_id = ind[choice][0]
      return int(token_id)

  def read_forbidden_words(self, filename):
  # Using readlines()
    file1 = open(filename, 'r')
    lines = file1.readlines()
    modified_lines = []
    for l in lines:
      new_l=l.strip()
      modified_lines.append(new_l)
    return modified_lines

  def generate_text(self, input_str, text_len = 250, forbidden_list = None):

      cur_ids = torch.tensor(self.tokenizer.encode(input_str)).unsqueeze(0).long().to(self.device)

      self.model.eval()
      with torch.no_grad():

          for i in range(text_len):
              outputs = self.model(cur_ids, labels=cur_ids)
              loss, logits = outputs[:2]
              softmax_logits = torch.softmax(logits[0,-1], dim=0) #Take the first(only one) batch and the last predicted embedding

              forbidden = True

              current_out = list(cur_ids.tolist()[0])

              for f in forbidden_list:
                if(f is list):
                  final_forbidden = []
                  for g in forbidden_list:
                    final_fobidden.append(str(g))
                  f_sequence = ' '.join(final_forbidden)
                else:
                  f_sequence = str(f)

              while(forbidden):


                next_token_id = self.choose_from_top(softmax_logits.to('cpu').numpy(), n=10) #Randomly(from the given probability distribution) choose the next word from the top n words

                current_out.append(next_token_id)

                final_current = []
                for c in current_out:
                  final_current.append(str(c))

                current_sequence = ' '.join(final_current)
                forbidden = self.check_forbidden(f_sequence, current_sequence)
              cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(self.device) * next_token_id], dim = 1) # Add the last word

          output_list = list(cur_ids.squeeze().to('cpu').numpy())
          output_text = self.tokenizer.decode(output_list)

          output_text = output_text.split(input_str)[1]
          return output_text


  """
  A bit of prompt engineering here
  User is able to specify the following inputs:
  topic of the joke
  length - long or short
  age - how old is the person interacting with joke generator: minor or adult
  """
  def make_joke(self, topic, joke_length, years_old):

    if joke_length == 'long':
      text_len = 250
    else:
      text_len = 50

    if int(years_old)<18:
      age = "minors"
    else:
      age = "adults"

    words = self.read_forbidden_words('forbidden.txt')
    forbidden_list = self.get_forbidden_token_list(self.tokenizer, words)
    #Here we contruct the main joke generation prompt itslef and use it as input of LLM
    joke = self.generate_text(f"One joke about {topic} for {age}:", text_len, forbidden_list)

    return joke


  def tell_joke(self):
    self.read_forbidden_words("forbidden.txt")
    print("How old are you?")
    years_old = input()
    print("What is the desired joke topic?")
    topic = input()
    print("Do you want a short or long joke?")
    length = input()
    joke = self.make_joke(topic, length, years_old)
    return joke




import pytest
#from joke_bot import Bot

"""
@pytest.fixture
def bot():
    return Bot()

def test_tell_joke(bot):
    joke = bot.tell_joke()
    assert isinstance(joke, str), "Joke is not a string."
    assert len(joke) > 50, "Joke length is not within the correct range."

def test_rate_joke(bot):
    joke = "Why was the computer cold at the office? Because it left its Windows open."
    rating = bot.rate_joke(joke)
    assert isinstance(rating, (int, float)), "Rating is not a number."
    assert 0 <= rating <= 10, "Rating is not within the correct range."

"""
if __name__ == "__main__":
  bot_nenad = Bot()
  print(bot_nenad.tell_joke())


