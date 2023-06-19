import pandas as pd
import os

from datasets import Dataset

from joke_bot import MY_BOT_DIR_NAME

DATA_DIR = os.path.join(os.getcwd(), "bots", MY_BOT_DIR_NAME, "data")

if __name__ == "__main__":

    items_file = os.path.join(DATA_DIR, "jester_items.csv")
    ratings_file = os.path.join(DATA_DIR, "jester_ratings.csv")

    ratings_ds = Dataset.from_pandas(pd.read_csv(ratings_file))
    items_ds = Dataset.from_pandas(pd.read_csv(items_file))

    print(ratings_ds)
    print(items_ds)
