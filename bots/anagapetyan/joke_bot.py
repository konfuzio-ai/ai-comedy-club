import os
import time

from openai import OpenAI


class Bot:
    def __init__(self, thread=None):
        self.client = OpenAI()

        self.assistant_path = "assistant.txt"

        self.assistant_id = self.load_assistant_id()
        if self.assistant_id:
            try:
                self.client.beta.assistants.retrieve(self.assistant_id)
            except:
                self.init_assistant()
        else:
            self.init_assistant()

        if thread:
            self.thread = thread
        else:
            self.thread = self.client.beta.threads.create()

    def init_assistant(self):
        new_assistant_id = self.client.beta.assistants.create(
                name="Comedy Assistant",
                instructions="You are one of the AI Comedy Club's member. \
                            You should have some level of interactivity, asking the user about their mood, \
                            their preference for joke types, and so on.\
                            DONT ASK me to estimate your joke \
                            When users message starts exatly with this construction 'Rate this joke for me with single integer number:' \
                            then rate the joke from 1 up to 10; you must only output a SINGLE NUMBER AND NOTHING ELSE, no more text for this case, just one number, 1, 2,3 4,5,6,7,8,9 or 10  \
                            ",
                model="gpt-3.5-turbo",
            ).id

        self.save_assistant_id(new_assistant_id)
        self.assistant_id = new_assistant_id

    def load_assistant_id(self):
        if os.path.exists(self.assistant_path):
            with open(self.assistant_path, "r") as file:
                return file.read().strip()
        return None

    def save_assistant_id(self, assistant_id):
        with open(self.assistant_path, "w") as file:
            file.write(assistant_id)
    
    def tell_joke(self, user_input):
        if user_input:
            return self.process_input(user_input)

    def rate_joke(self, joke, return_type=int):
        if joke:
            bot_output = self.process_input(joke, is_rating=True)
            if bot_output.endswith('.'):
                bot_output = bot_output[:-1]
            if return_type == int:
                return int(bot_output)
            else:
                return bot_output

    def process_input(self, user_input, is_rating=False):
        prefix = "Rate this joke for me with single integer number: " if is_rating else ""
        run = self.submit_message(f"{prefix}{user_input}")
        
        self.wait_on_run(run)
        response_messages = self.get_response().data
        return response_messages[-1].content[0].text.value

    def wait_on_run(self, run):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    def get_response(self):
        return self.client.beta.threads.messages.list(thread_id=self.thread.id, order="asc")
    
    def submit_message(self, user_message):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=user_message
        )
        return self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant_id,
        )
