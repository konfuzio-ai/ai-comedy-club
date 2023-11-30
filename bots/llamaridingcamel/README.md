# AI Comedian LLama riding Camel
An AI Comedian with a hilarious name LLama riding Camel made using `Mistral-7B-Instruct-v0.1`. 
This AI comedian can tell jokes on various topics such as children, men, women, business, office, 
doctor, shopping, etc. It not only tells jokes, but it can also rate other jokes based on humor, 
creativity, appropriate content, etc. This model fine-tuned on taivop's plain english jokes dataset
to tell jokes. 

## Prerequisite

This bot requires following python libraries:
```
transformers >= 4.32.0 
optimum >= 1.12.0
auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/
accelerate
peft
datasets
```

## Model

Base model for this Bot is `Mistral 7B Instruct v0.1 - GPTQ`, quantized 8bit version of the 
`Mistral-7B-Instruct-v0.1` model.

* Model: Mistral 7B Instruct v0.1 - GPTQ
* Revision: gptq-8bit-128g-actorder_True
* Required GPU RAM: 10GB

## Dateset

Joke Dataset, A dataset of English plaintext jokes. Cloned from the following repository.
```
https://github.com/taivop/joke-dataset
```

This repository contains a dataset of English plaintext jokes. There are about 208 000 jokes in this database scraped from three sources.

```
----------------------------------------------
reddit_jokes.json |  195K jokes | 7.40M tokens
stupidstuff.json  | 3.77K jokes |  396K tokens
wocka.json        | 10.0K jokes | 1.11M tokens
----------------------------------------------
TOTAL             |  208K jokes | 8.91M tokens
----------------------------------------------
```

`reddit_jokes` do not contain any additional information regarding the jokes, while `stupidstaff` and 
`wocka` contains additional information such as category, score, title etc related to joke. Which provides
useful information while creating prompt for joke telling and joke rating dataset. So I have used only
the jokes from `stupidstaff` and `wocka` with a maximum word length of 100. After all kind of cleaning and
filtering here is final dataset for fine-tuning.

| Dataset                   | Total Items |
|---------------------------| ----------- |
| stupidstaff joke telling  |	1566 |
| wocka joke telling        | 3773 |
| stupidstaff joke rating	  | 6512 | 
| Total                     | 11851 | 


Here are some samples:

```
[INST]Tell a joke about Men using keywords such as man, bar, husband, sports, guys, etc[/INST]

Here is a joke:
A young woman was taking an afternoon nap. After she woke up, she told her husband, "I just dreamed 
that you gave me a pearl necklace for Valentine's day. What do you think it means?""You'll know 
tonight." he said.That evening, the man came home with a small package and gave it to his wife. 
Delighted, she opened it-only to find a book entitled "The meaning of dreams".

----------------

[INST] Classify the humor level of a given joke in 5 classes. Output must be a class from one of very 
funny, funny, neutral, not funny, or sad. [/INST]

Joke: One day, a blonde's neighbor goes over to her house, sees the blonde crying, and asks her what 
happened. The blonde said that her mother had passed away. The neighbor made her some coffee and calmed 
her down a little and then left. The next day the neighbor went back over to the house and found the 
blonde crying again. She asked her why she was crying this time. ''I just got off of the phone with my 
sister, her mother died too!''
Rating: funny

```

## Fine-tuning / QLoRA

I have used LoRA to fine-tune `Mistral-7B-Instruct-v0.1` 8bit quantized model. LoRA config as follows:

```
r=16,
lora_alpha=32,
target_modules=["k_proj","o_proj","q_proj"],
lora_dropout=0.045,
```

Number of trainable params: `11,010,048` which is `4.026% `of all params. The model has been trained 
for `20` epochs. Fine-tuned model has been pushed to `huggingface`  as an additional adapter with
the name `rajesh06/mistral-7b-llama-riding-camel`. This model can be downloaded and used as an 
additional adapter to the `Mistral-7B-Instruct-v0.1-GPTQ` for joke telling and joke rating. To know more
follow the `finetune_mistral_7b_taivop_jokes_dataset.ipynb` notebook. To download the `peft model 
adapter` go to the following link:
```
https://huggingface.co/rajesh06/mistral-7b-llama-riding-camel
```

## Using the bot
```python
from joke_bot import Bot
bot = Bot()
```
Use bot `tell_joke()` function to get a AI generated joke.
```python
for i in range(3):
    joke = bot.tell_joke()
    print(joke)
    print("")
```
```
Hey, bros and sistas! LLama riding Camel in the virtual dojo, ready to drop some food wisdom on ya! 
Why did the bagel not win the race? It was too bagelled.

What's kickin', party people and laughter enthusiasts! LLama riding Camel in the comedy cockpit,
ready to take you on a hilarious joyride! Here to sprinkle some programming magic on your 
black n white life! 
Why did the Java programmer break up with his girlfriend? Because she was a JavaScript and he 
couldn't take it.

LLama riding Camel in the virtual dojo, here to sprinkle some food magic on your binary life! 
I asked the butcher to make a sandwich using only the best cuts of meat. He agreed, 
but only if I promised not to take it for granted.
```

`tell_joke` function also supports an optional parameter context. It then extracts the category, 
and keywords from the context and generates a joke related to the context using those keywords.

```python
joke = bot.tell_joke(context="Tell me joke about football or soccer")
```
```
LLama riding Camel in the virtual dojo, here to sprinkle some sports magic on your binary life! 
Bro, did you hear the one about the football player who wanted to be a soccer player? 
Bro: He couldn't decide to be a football player or a soccer player, so he became a quarterback!
```

### Evaluation of Jokes

* **Humor:** Generated jokes are humorous up to a certain level. Although more work can be done to make the jokes funnier.
* **Creativity:** Generated jokes are creative and unique.
* **Timeliness:** It is possible to incorporate current events or popular culture into the jokes by using the context.
* **Personalization:** This bot can tailor its jokes based on the user's preferences, past interactions, or known demographic information by using the context feature.
* **Tone and Style:** This bot maintains a certain comedic style. It always uses a broish style to tell its joke. Starts its jokes with things like Hey bro, Dude, etc and follows distinctive delivery.
* **User Engagement:** This AI comedian encourages interaction by asking questions in most of its jokes.
* **Appropriate Content:** All the jokes are appropriate by carefully avoiding racist or inappropriate puns. Every jokes are being generated after careful prompt engineering.
* **Diversity of Jokes:** The bot can create multiple categories of jokes. Right now it can create jokes from categories like 'social media', 'online shopping', 'netflix', 'sports', 'general', etc. More categories can be added to this list. Also wide varities of jokes can be generated by providing keywords to the joke. All of these things are managed dynamically through prompting.

To know how the joke telling works please follow the `bot_usage_examples.ipynb` notebook.

This bot is also capable of rating a joke. Use the `rate_joke` from the bot to rate a joke. Here are
some joke rating output.

```
Sandy’s mum has four kids; North, West, East. What is the name of the fourth child? Sandy, obviously!
rating: 8.12

I just had a huge breakfast. I have not feeling good since then.
rating: 4.09

Here is the best joke for you. I jumped, Then I changed my mind.
rating: 4.38
```

`rate_joke` function run the following operations to rate a joke:

* rate_sentiment_polarity
* detect_if_joke_contains_question
* detect_if_joke_contains_inappropriate_content
* rate_joke_humor

To know how the joke rating works please follow the `bot_usage_examples.ipynb` notebook.

## Future Works
* This bot is still not consistent while rating a joke. So one of the next step should be creating a joke
rating dataset from different sources such as, reddit jokes with number of likes. And fine-tune the model
using that dataset.
* The following short jokes dataset contains 231K jokes, but sadly it lacks any additional 
information, such as category or keywords to create a more instructive prompts for the LLM. <br/>
`https://www.kaggle.com/datasets/abhinavmoudgil95/short-jokes` <br/>
So, one step would be to extract category and keywords from these jokes using some larger LLM and crate
a short jokes dataset with such additional information. Then use these newly crated dataset on this 
model to make joke telling more precise.
* Use and fine-tune smaller models such as `facebook/opt-1.3b` using the created dataset to produce
simillar result.
* Create an evaluation process for the `tell_joke` and `rate_joke` outputs.


