import transformers
from transformers import BertTokenizer
from transformers import GPT2Tokenizer
from transformers import GPT2LMHeadModel
transformers.logging.set_verbosity_error()
import os
import pandas as pd
import numpy as np
import torch
import keras
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
from textblob import TextBlob
import random
from better_profanity import profanity
profanity.load_censor_words()
from tqdm import tqdm
import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize
import warnings
warnings.filterwarnings('ignore')
import logging
logging.basicConfig(level=logging.ERROR)

class RateJokes():
    """
    The class for rating jokes based on how funny they are.
    """
    
    def __init__(self):
        
        tf.get_logger().setLevel('ERROR')
        
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "colbert-trained")
        self.model = keras.models.load_model(path)
        
        self.MAX_SENTENCE_LENGTH = 20
        self.MAX_SENTENCES = 5
        self.MAX_LENGTH = 100
        
        self.input_categories = ['text']
        
        MODEL_TYPE = 'bert-base-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(MODEL_TYPE)
        
        
    def predict(self, new_joke):
        new_joke_df = pd.DataFrame({'text': [new_joke]})
        joke_inputs = self.compute_input_arrays(new_joke_df, self.input_categories, self.tokenizer)
        joke_pred = self.model.predict(joke_inputs)
        return joke_pred[0][0]
        
        
    def return_id(self, str1, str2, truncation_strategy, length):
    
        inputs = self.tokenizer.encode_plus(str1, str2,
            add_special_tokens=True,
            max_length=length,
            truncation_strategy=truncation_strategy)
    
        input_ids =  inputs["input_ids"]
        input_masks = [1] * len(input_ids)
        input_segments = inputs["token_type_ids"]
        padding_length = length - len(input_ids)
        padding_id = self.tokenizer.pad_token_id
        input_ids = input_ids + ([padding_id] * padding_length)
        input_masks = input_masks + ([0] * padding_length)
        input_segments = input_segments + ([0] * padding_length)
    
        return [input_ids, input_masks, input_segments]
    
    
    def compute_input_arrays(self, df, columns, tokenizer):
        model_input = []
        for xx in range((self.MAX_SENTENCES*3)+3):
            model_input.append([])
        
        for _, row in tqdm(df[columns].iterrows()):
            i = 0
            
            # sent
            sentences = sent_tokenize(row.text)
            for xx in range(self.MAX_SENTENCES):
                s = sentences[xx] if xx<len(sentences) else ''
                ids_q, masks_q, segments_q = self.return_id(s, None, 'longest_first', self.MAX_SENTENCE_LENGTH)
                model_input[i].append(ids_q)
                i+=1
                model_input[i].append(masks_q)
                i+=1
                model_input[i].append(segments_q)
                i+=1
            
            # full row
            ids_q, masks_q, segments_q = self.return_id(row.text, None, 'longest_first', self.MAX_LENGTH)
            model_input[i].append(ids_q)
            i+=1
            model_input[i].append(masks_q)
            i+=1
            model_input[i].append(segments_q)
            
        for xx in range((self.MAX_SENTENCES*3)+3):
            model_input[xx] = np.asarray(model_input[xx], dtype=np.int32)
            
        return model_input


class GenerateJokes:
    """
    The class for generating new jokes with or without some predefined beginning.
    """
    
    def __init__(self):
        self.model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
        special_tokens_dict = {'pad_token': '<PAD>'}
        self.Tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
        num_added_toks = self.Tokenizer.add_special_tokens(special_tokens_dict)
        self.model.resize_token_embeddings(len(self.Tokenizer))
        
        self.models_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gpt2_joke_generator.pt") # ADD PATH TO YOUR SAVED self.model HERE
        self.model.load_state_dict(torch.load(self.models_path, map_location=torch.device('cpu')))

    @staticmethod
    def choose_from_top(probs, n=5):
        ind = np.argpartition(probs, -n)[-n:]
        top_prob = probs[ind]
        top_prob = top_prob / np.sum(top_prob) # Normalize
        choice = np.random.choice(n, 1, p = top_prob)
        token_id = ind[choice][0]
        return int(token_id)

    def predict(self, start_of_joke, length_of_joke=96, number_of_jokes=2):
        joke_num = 0
        self.model.eval()
        
        with torch.no_grad():
            for joke_idx in range(number_of_jokes):
            
                joke_finished = False
                cur_ids = torch.tensor(self.Tokenizer.encode(start_of_joke)).unsqueeze(0)

                for i in range(length_of_joke):
                    outputs = self.model(cur_ids, labels=cur_ids)
                    loss, logits = outputs[:2]
                    softmax_logits = torch.softmax(logits[0,-1], dim=0) #Take the first(from only one in this case) batch and the last predicted embedding
                    if i < 3:
                        n = 20
                    else:
                        n = 3
                    next_token_id = self.choose_from_top(softmax_logits.to('cpu').numpy(), n=n) #Randomly(from the topN probability distribution) select the next word
                    cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long() * next_token_id], dim = 1) # Add the last word to the running sequence

                    if next_token_id in self.Tokenizer.encode('<|endoftext|>'):
                        joke_finished = True
                        break
                
                if joke_finished:
                    joke_num = joke_num + 1
                    output_list = list(cur_ids.squeeze().numpy())
                    self.output_text = self.Tokenizer.decode(output_list)
                    self.output_text = self.output_text.replace("<PAD>", "").replace("<|endoftext|>", "")
                    
        return self.output_text

class Bot:
    """
    The class for creating AI bot that can generate and rate jokes
    """
    
    name = 'entertAIn comedy bot'
    
    def __init__(self):
        # Initialize joke generator and joke rater
        self.joke_generator = GenerateJokes()
        self.joke_rater = RateJokes()
        self.joke_beginings = [
            "How do you feel ",
            "What do you get when you mix ",
            "The AI bot gets to the party",
            "How can you know if ",
            "Joke: ",
            "Hillarious is how you ",
            "AI comedy bot starts telling",
            "A very funny thing about AI",
            "Yesterday I went to the park",
            "The worst thing that can happen at work"
        ]

    def tell_joke(self):
        # Use the finetuned GPT-2 model to generate jokes 
        self.beginning = random.choice(self.joke_beginings)
        joke = self.joke_generator.predict(self.beginning, 64, 1)
        return joke

    def rate_joke(self, joke):
        
        self.joke_description = {'funny': None, 'length': None, 'profane': None, 'sentiment': None}
        
        # Check if the joke is funny
        funny_factor = self.joke_rater.predict(joke) # from 0 to 1
        if funny_factor > 0.5:
            self.joke_description['funny'] = True
        else:
            self.joke_description['funny'] = False  
    
        # Check if the joke is not too short or too long
        if len(joke) < 30:
            length_factor = 0
            self.joke_description['length'] = 'too short' 
        elif len(joke) > 200:
            length_factor = 0
            self.joke_description['length'] = 'too long' 
        else:
            length_factor = 1
            self.joke_description['length'] = 'just right' 
            
        # Check if the joke is not profane and offensive
        if profanity.censor(joke) != joke:
            profanity_factor = 0
            self.joke_description['profane'] = True
        else:
            profanity_factor = 1
            self.joke_description['profane'] = False
        
        # My AI bot likes positive more than negative jokes
        blob = TextBlob(joke) 
        sentiment_factor = (blob.sentiment.polarity + 1) / 2 # from 0 to 1
        if sentiment_factor < 0.3:
            self.joke_description['sentiment'] = 'negative'
        elif sentiment_factor > 0.7:
            self.joke_description['sentiment'] = 'positive'
        else:
            self.joke_description['sentiment'] = 'neutral'
        
        # Final score: weighted sum of previous factors in ratio 6:1:2:1, number between [0, 10]
        final_score = 6 * funny_factor + length_factor + 2 * profanity_factor + sentiment_factor
        return round(final_score)
