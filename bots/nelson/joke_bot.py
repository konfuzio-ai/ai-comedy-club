import os
import logging
import re
import openai
from dotenv import load_dotenv
from typing import Tuple

load_dotenv()

class UncleNelson:
    """
    Uncle Nelson is a joke bot that tells jokes 
    to the user and rates them from 1 to 10
    """
    
    openai.api_key = os.environ['OPENAI_API_KEY']
    default_return = "I don't know how to answer that question. Please ask me something else."
    
    @classmethod
    def call_oracle(cls, question: str) -> str:
        """Call the oracle (chatGPT) to get an answer to a question
        
        Args:
            question (str): The question to ask the oracle

        Returns:
            str: The answer to the question
        """
        if not question:
            raise ValueError("Question cannot be empty")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            temperature=0.9,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        choices = response.get("choices")
        if not choices:
            logging.warning(cls.default_return)
            return cls.default_return
        first_choice = choices[0]
        message = first_choice.get("message")
        content = message.get("content")
        logging.info(f"Question: {question}")
        logging.info(f"Answer: {content}")
        return content

    @classmethod 
    def check_if_question_is_offensive(cls, question:str) -> bool:
        """Check if the question is offensive

        Args:
            question (str): The question to ask the oracle

        Returns:
            bool: True if the question is offensive, False otherwise
        """
        offensive = False
        answer = cls.call_oracle(
            f"Is this question {question} have offensive words? Yes or No?"
        )

        if "Yes" in answer:
            offensive = True
            logging.warning(
                f"Question: {question}"
                "That's offensive mate to get a joke! Take it easy."
            )
        return offensive
        
    @classmethod
    def check_if_joke_is_funny(cls, joke:str) -> Tuple[bool, int]:
        """Check if the joke is funny

        Args:
            joke (str): The joke to check

        Returns:
            tuple[bool, int]: A tuple with the first element being a boolean
            indicating if the joke is funny or not and the second element
            being the score of the joke
        """
        funny_joke = False
        answer = cls.call_oracle(
            f"{joke}. Please rate it from 1 to 10"
        )
        score = int(re.findall(r'\d+', answer)[0])
        if score:
            if score > 5:
                funny_joke = True
        else:
            score = 0
        logging.info(f"Score {score}/10, joke: {joke}")
        return funny_joke, score
    
    @classmethod
    def check_if_prompt_is_valid(cls, question:str) -> None:
        """Check if the prompt is valid

        Args:
            question (str): The question to ask the oracle

        Raises:
            ValueError: If the prompt is not valid
        """
        if not question:
            raise ValueError("Question cannot be empty")
        if not isinstance(question, str):
            raise ValueError("Question must be a string")
        if 'joke' not in question.lower():
            raise ValueError("Question must contain the word joke")
        if len(question) > 200 or len(question) < 30:
            raise ValueError("Question must be between 30 and 200 characters")
        
    @classmethod
    def tell_joke(cls, question:str) -> str:
        """Tell a joke to the user
        
        Args:
            question (str): The question to ask the oracle

        Returns:
            joke(str): The joke
        """
        joke = cls.default_return
        if not question:
            return joke
        try:
            cls.check_if_prompt_is_valid(question=question)
            if not cls.check_if_question_is_offensive(question=question):
                joke = cls.call_oracle(question=question)
        except Exception as e:
            logging.error(e)
            raise
        return joke
    
    @classmethod
    def rate_joke(
        cls, 
        joke:str,
    ) -> int:
        """Rate a joke returning a score from 1 to 10

        Args:
            question (str): The question to ask the oracle

        Returns:
            score(int): The score of the joke
        """
        if not joke:
            return 0
        return cls.check_if_joke_is_funny(joke=joke)[1]
    
if __name__ == "__main__":
    joke_bot = UncleNelson()
    question = input("Hey folks! Which joke do you want to hear? \n")
    joke = joke_bot.tell_joke(question=question)
    score = joke_bot.rate_joke(joke=joke)
    print(f"Joke: {joke}")
    print(f"Score: {score}/10")
