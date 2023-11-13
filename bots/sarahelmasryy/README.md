# Joki





## Overview

Joki is the name of the chatbot which is Python script that generates and rates jokes using the pyjokes library. It evaluates jokes based on creativity and style, providing a rating for each joke.

## Getting Started


### Installation


 Install the required libraries using pip:

   ```bash
   pip install pyjokes networkx

   ```


## Usage

Run `test_bot.py` to start an interactive session with the bot:

```
python bots/sarahelmasryy/test_bot.py
```
To terminate the bot and exit the session, type 'quit' when prompted.
## Joke Generation

The bot utilizes the pyjokes library to randomly select jokes to tell. It also evaluates jokes based on:

- Creativity: By comparing to a knowledge graph of previously heard jokes 

- Style: By checking for engaging punctuation

## User Feedback

After each joke, the bot prompts the user to rate it. It averages the creativity and style scores to calculate an overall rating.

## Knowledge Graph

The file `creative_jokes_knowledge_graph.gml` contains a graph of previously heard jokes. This is used to gauge creativity when a new joke is encountered.

Future work will incorporate ratings into the graph to favor higher scoring material over time.

## My proposal

I don't want to add ChatGPT API or hugging face model API to solve the problem. I want to propose a solution using each criteria

Each critiea represent 1 point and we have 10 criterias to obtain in the end 10 points to rate the chatbot 


1. Humor: 

It uses natural language processing (NLP) and sentiment analysis to assess the humor of jokes based on user reactions and feedback. Integrate a rich dataset of jokes and humor styles to understand what's funny to different audiences
We can create a custom model to classify the humor level of the joke 


2. Creativity: 

Implement algorithms to generate jokes with different structures, punchlines, and styles. It is similar to the knowledge graph I did.

3. Timeliness:

Integrate APIs or sources for real-time news and pop culture references. We develop algorithms that can generate jokes about current events and trends. For example, we can use twitter API to discover what is trend.

4. Personalization: 

Tailor jokes to individual users using user profile and preference data. Implement reinforcement learning to adjust the comedian's style based on user interactions and feedback.

5.  Tone and style: 

AI Comedian's consistent comedy style allows her to define her style and maintain that style throughout her interactions.  Train your model using a variety of comedic voices and styles  for versatility. 


6. Adaptability: 

Implement reinforcement learning to adjust joke delivery and style based on user feedback and ratings.  Use machine learning models to adapt to your audience's sense of humor during conversations.

7. User Engagement:

Design an AI comedian that actively interacts with users through questions, prompts, and playful banter.  Encourage users to provide feedback and rate jokes to improve comedians' performance by using LangChain.

8. Appropriate Content:
Implement content filtering and moderation to ensure  jokes are appropriate for all viewers. Allow users to set content preferences or sensitivity levels. 


9. Diversity of Jokes: 

Train the model on a diverse dataset of jokes spanning various themes, cultures, and genres.  Ensure that the AI comedian can switch between different types of humor based on user preferences.

10. Delivery:
Pay attention to the timing, pacing, and phrasing of jokes to maximize their effectiveness.






   
