import os
from pathlib import Path
import pandas as pd
import pickle
from typing import List, Tuple, NewType
from sentence_transformers import SentenceTransformer
import torch


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
SBERT_MODEL_NAME: str = 'sentence-transformers/all-MiniLM-L12-v2'
# file taken from: https://raw.githubusercontent.com/amoudgl/short-jokes-dataset/master/data/reddit-cleanjokes.csv
JOKES_FILE: str = os.path.join(Path(__file__).parent, "data", "reddit-cleanjokes.csv")
PICKLE_DEST: str = os.path.join(Path(__file__).parent, "data", "embeddings_jokes.pkl")


Embedded_Jokes_Type = NewType('Embedded_Jokes_Type', List[Tuple[torch.Tensor, str]])
model_sbert = SentenceTransformer(
    SBERT_MODEL_NAME,
    device=DEVICE)


if __name__ == "__main__":
    jokes_from_file = pd.read_csv(JOKES_FILE)["Joke"].values.tolist()

    EMBEDDED_JOKES: Embedded_Jokes_Type = [(model_sbert.encode(joke), joke) for joke in jokes_from_file]

    # save our embeddings as list of (embeddings, jokes). This way we only have to compute them once.
    with open(PICKLE_DEST, "wb") as file:
        pickle.dump(EMBEDDED_JOKES, file)
