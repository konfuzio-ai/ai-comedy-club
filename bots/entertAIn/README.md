# entertAIn comedy bot

Hello everyone! This is the first AI standup comedy ever!

My name is entertAIn - AI bot designed to entertain you :D


## Installation

To be able to run entertAIn comedy bot functionalities, first you need to install all the necessary libraries by running this command: 

```
pip install -r requirements.txt
```

Next, you need to download the pretrained models and put them in this folder.

Download the pretrained model and name it "gpt2_joke_generator.pt" for joke generation:

https://drive.google.com/file/d/1-TMmXRXmbIqaHxF6gdoTmsFNlcy97LPx/view?usp=sharing

Download the whole "colbert-trained" folder for joke rating:

https://drive.google.com/drive/folders/1QLOsAa1tkmBKuQgIViGVdwOSLd5pQcYU?usp=sharing

![image](https://github.com/VukIlic/ai-comedy-club/assets/135129982/7bc2c527-9967-4573-9ae8-6df6470840d8)

The final content of the folder should look like this:

![image](https://github.com/VukIlic/ai-comedy-club/assets/135129982/17e0878b-4553-49bb-a93e-97ffbb5cc921)

## Joke Generation Training

Jokes_Generation.ipybn is Jupyter notebook for training Joke Generation Model. You need to provide config.py file to the same folder where you ran your notebook. In the config.py file you can define the path to your dataset. The jokes are located in the dataset/shortjokes.csv. That's the dataset from this link:

https://www.kaggle.com/datasets/abhinavmoudgil95/short-jokes

The original dataset contains 231,657 jokes. That dataset is filtered so I hope it doesn't contain inappropriate jokes. After the filtering
the dataset contains 175,445 jokes.

! The saved model will be stored in gpt2_joke_generator.pt so you don't have to run this code.

## Joke Generation Testing 

The joke generation is provided in the GenerateJokes class in the joke_bot.py file. The scripts loads pretrained model from gpt2_joke_generator.pt file.

To interract with entertAIn comedy bot you can run the user_interaction.py script. The bot will start to write some jokes in the CLI, ask you for
some answers, ratings and so on. 

## Results

The entertAIn is sometimes funny and sometimes he's not in the mood... But he's alway trying his best :D

Here are some results of interesting generated jokes:

What do you get when you mix AI bot and funny people? An adorable little bot that's just a little too cute for its own good.

What do you call a man who can't stop talking about his wife? A man who's never been married.

Why do you think about funny jokes at work? Because if you don't, they'll be all over the place.

What do you get when you cross a dog and a cat? A cat and an angry dog.

When is the perfect time to get in a fight? When it's not too hot.

How do you know when you're being "watched"? You know the time.

# Joke Rating
To calculate joke rate we calculate few factors:

1. funny_factor - if the joke is classified as funny or not (number between 0 and 1)
   
funny_factor is calculated from pretrained model described on this link:

https://github.com/Moradnejad/ColBERT-Using-BERT-Sentence-Embedding-for-Humor-Detection

It follows the paper called "ColBERT: Using BERT Sentence Embedding in Parallel Neural Networks for Computational Humor" for classification if 
the text is considered joke or not, which you can find on this link:

https://arxiv.org/abs/2004.12765

The dataset was composed of 200,000 formal short texts with label 'funny' and 'not funny'.

funny_factor is calculated in RateJokes class in the joke_bot.py script.

2. length_factor - if the joke is not too short or too long (0 for too long or too short, 1 for just right)

3. profanity_factor - if the joke is not profane (0 for profane, 1 for not profane)

4. sentiment_factor - likes positive more than negative jokes (nuber between 0 and 1)
   
The final score is calculated as weighted sum of previous factors in ratio 6:1:2:1 (number between 0 and 10)




 



