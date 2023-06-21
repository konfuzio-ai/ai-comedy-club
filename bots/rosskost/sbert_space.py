from sentence_transformers import util
import random
import torch
import pickle
from typing import List

from bots.rosskost.enum_definitions import Topic
from bots.rosskost.save_joke_embeddings import (model_sbert,
                                                PICKLE_DEST,
                                                Embedded_Jokes_Type)

# load saved embeddings [they were saved and computed in save_joke_embeddings.py]:
with open(PICKLE_DEST, "rb") as file:
    jokes_from_file: Embedded_Jokes_Type = pickle.load(file)


def find_closest_joke_for_topic(topic: Topic, available_jokes: List[str], choice_from_top_n: int) -> str:
    """This function returns from the list of jokes a joke, that is close
    to the topic in the latent space of our language sentence-transformer model.
    To make it not return the same joke everytime, we randomly choose
    from the "choice_from_top_n"-most_similar jokes."""

    _embed_topic: torch.Tensor = model_sbert.encode(topic.value, convert_to_tensor=True)

    _list_sims_for_jokes = [(util.cos_sim(_embed_topic, _embed_joke).item(), joke)
                            for _embed_joke, joke in jokes_from_file if joke in available_jokes]

    if not _list_sims_for_jokes:
        raise ValueError(f"No jokes in list of embedded jokes: {_list_sims_for_jokes}")
    if len(_list_sims_for_jokes) < choice_from_top_n:
        raise ValueError(f"Not enough items to choose from. choice_from_top_n {choice_from_top_n } not >=len_embedded_jokes {len(_list_sims_for_jokes)} ")

    _sorted_n = sorted(_list_sims_for_jokes, key=lambda x: x[0], reverse=True)[0:choice_from_top_n]

    return random.choice([i[1] for i in _sorted_n])
