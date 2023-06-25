!pip install transformers

import logging
logging.getLogger().setLevel(logging.CRITICAL)

import torch
import numpy as np

from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import AdamW, get_linear_schedule_with_warmup


from transformers import pipeline
from textblob import TextBlob
import random

from csv import writer

from torch.utils.data import Dataset
from torch.utils.data import Dataset, DataLoader
import os
import json
import csv


class Utils():
    def append_rating_to_csv(self, name, joke, rating):
      List = [name, joke, rating]
 
      with open('ratings.csv', 'a') as f_object:

        writer_object = writer(f_object)
 
        # Pass the list as an argument into
        writer_object.writerow(List)
 
        # Close the file object
        f_object.close()

"""
This is the Jokes dataset class for model customization on jokes datasets
"""
class JokesDataset(Dataset):
    def __init__(self, jokes_dataset_path):
        super().__init__()

        #short_jokes_path = os.path.join(jokes_dataset_path, jokes_dataset_path)

        self.joke_list = []
        self.end_of_text_token = "<|endoftext|>"
        
        with open(jokes_dataset_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            x = 0
            for row in csv_reader:
                joke_str = f"JOKE:{row[1]}{self.end_of_text_token}"
                self.joke_list.append(joke_str)
        
    def __len__(self):
        return len(self.joke_list)

    def __getitem__(self, item):
        return self.joke_list[item]



"""
This is the main joker bot class based on GPT2 from transformers
"""
class Bot:
  def __init__(self):
    """
    self.joke_generator = pipeline('text-generation', model='gpt2')
    self.joke_prefixes = [
      "My best joke is: "
    ]

    """
    self.name = 'Nenad'

    self.device = 'cpu'
    if torch.cuda.is_available():
      self.device = 'cuda'

    self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    self.model = GPT2LMHeadModel.from_pretrained('gpt2')
    self.model = self.model.to(self.device)
    self.utils = Utils()

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
                    final_forbidden.append(str(g))
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
      text_len = 25

    if int(years_old)<18:
      age = "minors"
    else:
      age = "adults"

    words = self.read_forbidden_words('forbidden.txt')
    forbidden_list = self.get_forbidden_token_list(self.tokenizer, words)
    #Here we contruct the main joke generation prompt itslef and use it as input of LLM
    joke = self.generate_text(f"One joke about {topic} for {age}:", text_len, forbidden_list)

    return joke

  """
  This variant does not involve user input
  """
  def make_joke_default(self):
    words = self.read_forbidden_words('forbidden.txt')
    forbidden_list = self.get_forbidden_token_list(self.tokenizer, words)
    joke = self.generate_text(f"My best joke is:", 25, forbidden_list)
    return joke


  """
  In interactive mode, user input is taken into account
  Rating can be enabled/disabled
  """
  def tell_joke(self, interactive_mode=False, rating=False):
    self.model.eval()
    if interactive_mode:
      self.read_forbidden_words("forbidden.txt")
      print('What is your name?')
      name = input()
      print("How old are you?")
      years_old = input()
      print("What is the desired joke topic?")
      topic = input()
      print("Do you want a short or long joke?")
      length = input()
      joke = self.make_joke(topic, length, years_old)
      print(joke)
      if rating:
        print("Rate this joke")
        rate = input()
        self.utils.append_rating_to_csv(name, joke, rate)
    else:
      joke = self.make_joke_default()
    return joke

  """
  Customizes the model by additional training on jokes dataset, such as shortjokes.csv
  """
  def train(self, jokes_dataset_path='./shortjokes.csv', BATCH_SIZE = 16, EPOCHS = 5, LEARNING_RATE = 3e-5, WARMUP_STEPS = 5000, MAX_SEQ_LEN = 400):
    dataset = JokesDataset(jokes_dataset_path)
    joke_loader = DataLoader(dataset, batch_size=1, shuffle=True)
    self.model = self.model.to(self.device)
    self.model.train()
    optimizer = AdamW(self.model.parameters(), lr=LEARNING_RATE)

    # Calculate the value of num_training_steps
    #t_total = int(len(joke_loader) * EPOCHS)
    t_total = -1

    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=WARMUP_STEPS, num_training_steps = t_total)
    proc_seq_count = 0
    sum_loss = 0.0
    batch_count = 0

    tmp_jokes_tens = None
    models_folder = "trained_models"
    if not os.path.exists(models_folder):
        os.mkdir(models_folder)

    for epoch in range(EPOCHS):
        
        print(f"EPOCH {epoch} started" + '=' * 30)
        
        for idx,joke in enumerate(joke_loader):
            #################### "Fit as many joke sequences into MAX_SEQ_LEN sequence as possible" logic start ####
            joke_tens = torch.tensor(self.tokenizer.encode(joke[0])).unsqueeze(0).to(self.device)
            #Skip sample from dataset if it is longer than MAX_SEQ_LEN
            if joke_tens.size()[1] > MAX_SEQ_LEN:
                continue
            
            #The first joke sequence in the sequence
            if not torch.is_tensor(tmp_jokes_tens):
                tmp_jokes_tens = joke_tens
                continue
            else:
                #The next joke does not fit in so we process the sequence and leave the last joke 
                #as the start for next sequence 
                if tmp_jokes_tens.size()[1] + joke_tens.size()[1] > MAX_SEQ_LEN:
                    work_jokes_tens = tmp_jokes_tens
                    tmp_jokes_tens = joke_tens
                else:
                    #Add the joke to sequence, continue and try to add more
                    tmp_jokes_tens = torch.cat([tmp_jokes_tens, joke_tens[:,1:]], dim=1)
                    continue
            ################## Sequence ready, process it trough the model ##################


            outputs = self.model(work_jokes_tens, labels=work_jokes_tens)

            loss, logits = outputs[:2]                        
            loss.backward()
            sum_loss = sum_loss + loss.detach().data
            print(f"sum loss {sum_loss}")
                          
            proc_seq_count = proc_seq_count + 1
            if proc_seq_count == BATCH_SIZE:
                proc_seq_count = 0    
                batch_count += 1
                optimizer.step()
                scheduler.step() 
                optimizer.zero_grad()
                self.model.zero_grad()

            if batch_count == 100:
                print(f"sum loss {sum_loss}")
                batch_count = 0
                sum_loss = 0.0
        # Store the model after each epoch to compare the performance of them
        torch.save(self.model.state_dict(), os.path.join(models_folder, f"gpt2_joker_{epoch}.pt"))

  """
  Load weight of a pre-trained model from given file
  """
  def load_state(self, models_folder="trained_models", weights_file="gpt2_joker_0.pt"):
    model_path = os.path.join(models_folder, weights_file)
    self.model.load_state_dict(torch.load(model_path))
 
if __name__ == "__main__":
  bot_nenad = Bot()
  
  #Datasets are needed for this
  #bot_nenad.train('./jokes_data/shortjokes.csv')
  
  #Load previously saved model weights
  #bot_nenad.load_state("trained_models", "gpt2_joker_0.pt")
  
  #Automatic no-interaction joke
  print(bot_nenad.tell_joke())
  
  #Interactive, no rating
  #print(bot_nenad.tell_joke(True, False))
  
  #Interactive with rating
  print(bot_nenad.tell_joke(True, True))

