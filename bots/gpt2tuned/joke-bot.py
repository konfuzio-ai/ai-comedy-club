import gpt_2_simple as gpt2
import os
import configparser
from datetime import datetime
import tokenize
config = configparser.ConfigParser()
config.read(os.path.join("fine-tuning", "conf.ini"))
run_name = config["DEFAULT"]["RunName"]

checkpoint_dir = os.path.join(os.getcwd(), "fine-tuning", "checkpoint")
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint_dir=checkpoint_dir, run_name=run_name)


class Bot():
    def text_generation(self) -> str:
        text = gpt2.generate(sess, checkpoint_dir=checkpoint_dir, run_name=run_name, length=50, return_as_list=True)
        return text[0]

    def rate_joke(self, joke):

        text = ("Málinu var vísað til stjórnskipunar- og eftirlitsnefndar "
                "skv. 3. gr. XVII. kafla laga nr. 10/2007 þann 3. janúar 2010.")

        for token in tokenize(text):
            print(token)
        return


def main():
    print(f"Greetings and have a good {datetime.now().strftime('%A')}! Want some jokes?")


if __name__ == "__main__":
    main()
