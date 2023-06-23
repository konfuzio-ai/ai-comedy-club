from bots.zumabot.comedian_bot import ComedianBot
from bots.zumabot.judge_bot import JudgeBot
import random


class Bot(ComedianBot, JudgeBot):
    def __init__(self):
        ComedianBot.__init__(self)
        JudgeBot.__init__(self)


if __name__ == "__main__":
    bot = Bot()
    bot.study_new_jokes()

    # Performance simulation 1
    bot.select_current_show_jokes()

    bot.introduce_comedian()
    for i in range(10):
        print(bot.tell_joke())
        comment = random.choice(["really good", "bad", "amazing"])
        bot.notice_feedback(comments=[comment])
        print(bot.current_joke_rating)
        bot.add_joke_rating()

    print(len(bot.jokes))
    bot.rate_joke("What's the difference between")
    print(len(bot.jokes))  # This bot learn jokes when it rates a joke
    # , and it can use it in the future as a comedian
    bot.finish_show()