from sentence_transformers import util
import random
import torch
import pickle

from enum_definitions import Topic
from save_joke_embeddings import (model_sbert,
                                  PICKLE_DEST,
                                  Embedded_Jokes_Type)

with open(PICKLE_DEST, "rb") as file:   # load saved embeddings:
    jokes_from_file: Embedded_Jokes_Type = pickle.load(file)


def find_closest_joke_for_topic(topic: Topic, choice_from_top_n: int = 4) -> str:
    """This function returns from the list of Jokes a random choice from the choice_from_top_n-most_similar
    jokes to the topic in the latent space of our language sentence-transformer model"""

    _embed_topic: torch.Tensor = model_sbert.encode(topic.value, convert_to_tensor=True)

    _list_sims_for_jokes = [(util.cos_sim(_embed_topic, _embed_joke).item(), joke)
                            for _embed_joke, joke in jokes_from_file]

    _sorted_n = sorted(_list_sims_for_jokes, key=lambda x: x[0], reverse=True)[0:choice_from_top_n]
    return random.choice([i[1] for i in _sorted_n])
