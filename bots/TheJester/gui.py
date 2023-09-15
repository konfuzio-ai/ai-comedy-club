"""
This Python code defines a function called response that responds to messages with a joke.

The function takes a message as input and uses the Bot class to generate a joke. The joke is then sent back to the user.

The function uses the chainlit library to send messages.
"""
from joke_bot import Bot
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
    response = bot.tell_joke(message)
    rating = bot.rate_joke(message)
    try:
        if 1 <= float(rating) <= 10:
            await chainlit.Message(content=response + f" I'd rate it {rating} out of 10.").send()
    except:
        await chainlit.Message(content=response).send()
