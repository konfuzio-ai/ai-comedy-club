"""
This Python code defines a function called response that responds to messages with a joke.

The function takes a message as input and uses the Bot class to generate a joke. The joke is then sent back to the user.

The function uses the chainlit library to send messages.
"""
from .joke_bot import Bot
import chainlit

bot = Bot()

@chainlit.on_message
async def response(message: str):
    """
    Responds to a message with a joke.

    Args:
        message: The message to be responded to.

    Returns:
        None.
    """
    await chainlit.Message(content=bot.tell_joke(message)).send()