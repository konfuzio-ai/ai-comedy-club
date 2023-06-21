import gpt_2_simple as gpt2
import os
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read(os.path.join("fine-tuning", "conf.ini"))
run_name = config["DEFAULT"]["RunName"]

checkpoint_dir = os.path.join(os.getcwd(), "fine-tuning", "checkpoint")
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint_dir=checkpoint_dir, run_name=run_name)


def text_generation() -> str:
    text = gpt2.generate(sess, checkpoint_dir=checkpoint_dir, run_name=run_name, length=50, return_as_list=True)
    return text[0]


def main():
    print(f"Greetings and have a good {datetime.now().strftime('%A')}! Want some jokes?")
    print(text_generation())


if __name__ == "__main__":
    main()
