from enum_definitions import Topic
from joke_bot import Bot

test_bot = Bot(
    topic=Topic.POLITICS,
)

print(test_bot.tell_joke(topic=Topic.RELATIONSHIPS))
