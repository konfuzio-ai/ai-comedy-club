from .joke_bot import Bot


def test_tell_joke(bot: Bot):
    for char in bot.tell_joke():
        print(char, end='')


def test_rate_joke(bot: Bot, joke: str):
    response = ''
    for char in bot.rate_joke(joke):
        response += char
        print(char, end='')
    return response


def main():
    load_in_8bit = False
    bot = Bot(load_in_8bit)
    print('Let me tell you a joke :')
    test_tell_joke(bot)
    print('Now give me a joke so i can rate your joke')
    test_rate_joke(bot, input('> '))


if __name__ == "__main__":
    main()
