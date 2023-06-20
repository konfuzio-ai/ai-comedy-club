from styles_and_topics import Codemian_Style, Topics
from joke_bot import Bot

test_bot = Bot(
    rating_model=None,
    style=Codemian_Style.KEVIN_HART,
    topic=Topics.POLITICS,
    name="b"
)


print(test_bot.get_prompt)
print(test_bot.tell_joke)