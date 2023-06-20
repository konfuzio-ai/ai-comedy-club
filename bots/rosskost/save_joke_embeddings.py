import os
from pathlib import Path
import pandas as pd
from typing import List, Tuple, NewType
import torch
import pickle
from sentence_transformers import SentenceTransformer


CACHE_DIR: str = os.sep.join(["D:", "model_cache"])
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
SBERT_MODEL_NAME: str = 'sentence-transformers/all-MiniLM-L12-v2'

model_sbert = SentenceTransformer(
    SBERT_MODEL_NAME,
    device=DEVICE,
    cache_folder=CACHE_DIR)


Embedded_Jokes_Type = NewType('Embedden_Jokes_Type', List[Tuple[torch.Tensor, str]])
PICKLE_DEST: str = os.path.join(Path(__file__).parent, "data", "embeddings_jokes.pkl")


if __name__ == "__main__":
    JOKES_FILE: str = os.path.join(Path(__file__).parent, "data", "funjokes.csv")
    jokes_from_file = pd.read_csv(JOKES_FILE)["Joke"].values.tolist()

    EMBEDDED_JOKES: Embedded_Jokes_Type = [(model_sbert.encode(joke), joke) for joke in jokes_from_file]

    with open(PICKLE_DEST, "wb") as file:  # save our embeddings as list of (embeddings, jokes)
        pickle.dump(EMBEDDED_JOKES, file)
