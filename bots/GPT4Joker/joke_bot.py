import random
import openai
import ast

class Bot:
    name = 'GPT4Joker'
    def __init__(self):
        self.api = openai
        self.api.api_key = 'YOUR_OPENAI_KEY'

    def tell_joke(self):
        messages = [
            {"role": "system", "content": 'You are a witty assistant that generates jokes based on user preferences and feelings. Your goal is to generate joke based on user message, if it is traffic, joke must be about traffic'},
            {"role": "assistant", "content": '{"joke":"no", "message": "How are you feeling today?"}'},
            {"role": "user", "content": "Good, but weather is a little bit bad..."},
            {"role": "assistant", "content": '{"joke": "yes": "message": "What do you call a month\'s worth of rain? England, hahahahaha}'},
            {"role": "user", "content": "HAHA, good one!"},
            {"role": "assistant", "content": '{"joke":"no", "message": "How are you feeling today?"}'},
        ]

        joke_generated = False
        while not joke_generated:
            print(ast.literal_eval(messages[-1]['content'])['message'])  # Display the last message from the assistant

            user_message = input("You: ")  # Get the user's input
            messages.append({"role": "user", "content": user_message})  # Append the user message

            response = self.api.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=150
            )

            assistant_message = response['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": assistant_message})  # Append the assistant's response

            # Check if the conversation should end (you can implement your own conditions)
            if ast.literal_eval(assistant_message)['joke'] == 'yes':
                joke_generated = True
            else:
                ast.literal_eval(messages[-1]['content'])['message'] += ' Can you tell me more?'

        return ast.literal_eval(assistant_message)['message']
    def rate_joke(self, joke):
        response = self.api.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 'You are a joke rater. return response as json. {"rate": 6}'},
                {"role": "user", "content": joke},
            ]
        )
        joke = response['choices'][0]['message']['content']
        return ast.literal_eval(joke)['rate']