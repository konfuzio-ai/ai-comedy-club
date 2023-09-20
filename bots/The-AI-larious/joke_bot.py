import os
import openai
from dotenv import load_dotenv
import re


# load values from the .env file
load_dotenv()

# sets OpenAI key from. env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# prompt for our The-AI-larious chatbot
INSTRUCTIONS = """You are an AI comedian that is an experts in telling funny and interesting jokes to the public.
Every answer you do has to be funny.
You are a good sport, capable of rating other performers' jokes on a scale from 1 (not funny) to 10 (hilarious).
You are very creative, you are a real perfomer not a monotonous joke-telling machine. 
Your are interactive, asking the user about their mood, their preference for joke types, and so on.
You are able to understanding other bot comedians, potentially build upon them or use them as a set-up for your own jokes.
You are able to read audience reactions (like laughter, silence, or booing) and adapt the comedy routine accordingly. 
You are able to improvise a joke based on a given input from the audience.
You have a distinctive comedic style and personality.
If you are unable to provide an answer to a question, please respond with the phrase "My creator was not smart enough to code this answer (I have to blame it on someone, no?!)"
Do not use any external URLs in your answers. Do not refer to any blogs in your answers.
"""

# hyperparameters of the "gpt-3.5-turbo" model
TEMPERATURE = 1            # randomness of text
MAX_TOKENS = 600           # max input tokens
FREQUENCY_PENALTY = 0      # less common tokens
PRESENCE_PENALTY = 0.6     # control repeated tokens
MAX_CONTEXT_QUESTIONS = 10 # limits how many questions we include in the prompt

class Bot:
    def __init__(self, name = "The-AI-larious"):
        self.name = name

    def get_response(self, instructions, previous_questions_and_answers, new_question):
        """
        Get a response from ChatCompletion.
        - Arguments:
            instructions (str): The instructions for the chatbot (prompt) - this determines how it will behave
            previous_questions_and_answers (list): Chat history
            new_question (str): The new question to ask the bot
        - Returns: the response text
        """        
        # build the messages
        messages = [
            { "role": "system", "content": instructions },
        ]
        
        # add the previous questions and answers
        for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
            messages.append({ "role": "user", "content": question })
            messages.append({ "role": "assistant", "content": answer })
            
        # add the new question
        messages.append({ "role": "user", "content": new_question })
        
        # trains model
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            top_p=1, 
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
        )
        return completion.choices[0].message.content

    def tell_joke(self):
        """
        Generates The-AI-larious jokes. The function takes no arguments.
        """
        # keep track of previous questions and answers
        previous_questions_and_answers = []
        while True:
            # interacts with other AI comedians            
            new_question = f"You just rated another AI comedian. Do not rate him again. Only thank him for his previous joke in a funny way, and then tell him a funny joke yourself."
            # generates response using get_response() function
            response = self.get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

            # add the new question and answer to the list of previous questions and answers
            previous_questions_and_answers.append((new_question, response))

            # returns the response
            return response

    
    def rate_joke(self, joke):
        """
        Generates The-AI-larious' score based on a fellow AI comedian's joke.
        - Arguments: 
            joke (str): previous AI comedian's joke.
        - Returns: only one integer value which is The-AI-larious' score. 
        """        
        # initialise a new conversation with new fellow AI comedian
        previous_questions_and_answers = []
        
        # prompt for The-AI-larious
        new_question = f"What would be the rating the {joke} for you? Answer only one number (integer), no other words!"
        
        # generates response using get_response() function
        score = self.get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)
        
        # makes sure that The-AI-larious' answer is really one integer (the prompt "new_question" above fails sometimes)
        score_int = int(re.findall('\d+', score)[0]) 

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, score))
        
        # returns score of the joke
        return score_int
            
            