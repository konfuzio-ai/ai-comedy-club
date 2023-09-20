from joke_bot import UncleNelson
import pytest
from unittest.mock import patch, Mock
class TestUncleNelson:

    def test_call_oracle_no_question(self):
        """
        Test that the call_oracle method returns None if no question
        is passed
        """
        with pytest.raises(ValueError):
            UncleNelson.call_oracle(None)

    @patch('openai.ChatCompletion.create')
    def test_call_oracle_no_choice(self, mock_ChatCompletion: Mock):
        """
        Test that the call_oracle method returns None if there 
        are no choices from API response
        """
        response = {"test": "No choices response"}
        mock_ChatCompletion.return_value = response
        content = UncleNelson.call_oracle("Is this a test?") 
        mock_ChatCompletion.assert_called_once_with(
            model="gpt-3.5-turbo-0613",
            temperature=0.9,
            messages=[
                {"role": "user", "content": "Is this a test?"}
            ]
        )
        msg = "I don't know how to answer that question. "
        msg += "Please ask me something else."
        assert content == msg

    @patch('openai.ChatCompletion.create')
    def test_check_if_question_is_offensive(self, mock_ChatCompletion: Mock):
        """
        Test that the check_if_question_is_offensive method returns True
        if the answer from the oracle is Yes to offensive question
        """
        mock_ChatCompletion.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Yes"
                    }
                }
            ]
        }
        audience = "Tell me a joke about war."
        question = f"Is this question {audience} have offensive words? Yes or No?"
        assert UncleNelson.check_if_question_is_offensive(
            question=question
        ) == True

    @patch('openai.ChatCompletion.create')
    def test_check_if_question_is_not_offensive(self, mock_ChatCompletion: Mock):
        """
        Test that the check_if_question_is_not_offensive method raises
        OffensiveQuestion exception if the answer from the oracle is Yes
        """
        mock_ChatCompletion.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "No"
                    }
                }
            ]
        }
        audience = "Tell me a joke about orange."
        question = f"Is this question {audience} have offensive words? Yes or No?"
        assert UncleNelson.check_if_question_is_offensive(
            question=question
        ) == False

    @patch('openai.ChatCompletion.create')
    def test_check_if_joke_is_funny(self, mock_ChatCompletion: Mock):
        """
        Test that the check_if_joke_is_funny method returns funny
        flag and score if the answer from the oracle is Yes
        """
        mock_ChatCompletion.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Yes. I give you 7!"
                    }
                }
            ]
        }
        assert UncleNelson.check_if_joke_is_funny(
            "Tell me a joke about laughter."
            ) == (True, 7)

    @patch('openai.ChatCompletion.create')
    def test_check_if_joke_is_not_funny(self, mock_ChatCompletion: Mock):
        """
        Test that the check_if_joke_is_funny method returns funny
        flag and score if the answer from the oracle is Yes
        """
        mock_ChatCompletion.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Yes. I give you 4!"
                    }
                }
            ]
        }
        assert UncleNelson.check_if_joke_is_funny(
            "Tell me a joke about ai."
            ) == (False, 4)

    def test_check_if_prompt_is_valid_no_question(self):
        """
        Test that the check_if_prompt_is_valid method raises
        ValueError if no question is passed
        """
        with pytest.raises(ValueError) as e:
            UncleNelson.check_if_prompt_is_valid(None)
        assert e.value.args[0] == "Question cannot be empty"

    def test_check_if_prompt_is_valid_question_not_string(self):
        """
        Test that the check_if_prompt_is_valid method raises
        ValueError if question is not a string
        """
        with pytest.raises(ValueError) as e:
            UncleNelson.check_if_prompt_is_valid(11)
        assert e.value.args[0] == "Question must be a string"

    def test_check_if_prompt_is_not_valid_short_question(self):
        """
        Test that the check_if_prompt_is_valid method raises
        ValueError if question is too short
        """
        with pytest.raises(ValueError) as e:
            UncleNelson.check_if_prompt_is_valid("joke "*5)
        assert e.value.args[0] == "Question must be between 30 and 200 characters"
    
    def test_check_if_prompt_is_not_valid_long_answer(self):
        """
        Test that the check_if_prompt_is_valid method raises
        ValueError if question is too long
        """
        with pytest.raises(ValueError) as e:
            UncleNelson.check_if_prompt_is_valid("Tell me about life in joke"*100)
        assert e.value.args[0] == "Question must be between 30 and 200 characters"

    def test_check_if_prompt_is_not_valid_no_joke_word(self):
        """
        Test that the check_if_prompt_is_valid method raises
        ValueError if question does not contain the word joke
        """
        with pytest.raises(ValueError) as e:
            UncleNelson.check_if_prompt_is_valid("Tell me about life in mars")
        assert e.value.args[0] == "Question must contain the word joke"

    @patch('openai.ChatCompletion.create')
    @patch('joke_bot.UncleNelson.check_if_question_is_offensive')
    def test_tell_joke(
        self,
        mock_check_if_question_is_offensive: Mock, 
        mock_ChatCompletion: Mock):
        """
        Test that the tell_joke method returns None if everything
        worked as expected and joke was funny
        """
        question = "Hey! Is this a test? Tell any joke"
        mock_ChatCompletion.side_effect = [
            {
                "choices": [
                    {
                        "message": {
                            "content": f"I can't think of a joke about: {question}"
                        }
                    }
                ]
            }
        ]
        mock_check_if_question_is_offensive.return_value = False
        msg = "I can't think of a joke about: Hey! Is this a test? Tell any joke"
        assert UncleNelson.tell_joke(question) == msg
        
    @patch('openai.ChatCompletion.create')
    def test_rate_joke(self, mock_ChatCompletion: Mock):
        """
        Test that the rate_joke method returns a score
        greater than 5 if the answer from the oracle is Yes
        """
        mock_ChatCompletion.side_effect = [
            {
                "choices": [
                    {
                        "message": {
                            "content": "Yes. I give you 7!"
                        }
                    }
                ]
            }
        ]
        assert UncleNelson.rate_joke("Hey! Is this a test?") == 7
