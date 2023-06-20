from sentence_transformers import SentenceTransformer, util
from joke_bot import available_jokes

from typing import List, TypeVar, NewType, Tuple
import torch
import os

from joke_bot import Topic


# is this necessary to explicitly call this embedding, decide later?
Embedding_Type = NewType("Embedding_Type", List[torch.Tensor])


CACHE_DIR: str = f"D:{os.sep}model_cache"


# all-MiniLM-L12-v2
model_sim = SentenceTransformer(
    'sentence-transformers/all-MiniLM-L12-v2',
    device="cpu",
    cache_folder=CACHE_DIR)


EMBEDDED_JOKES: List[Tuple[Embedding_Type, str]] = [(model_sim.encode(joke), joke) for joke in available_jokes]


def get_bert_sim_score(caption1: str, caption2: str) -> float:
    """"
    This function returns the sentence similarity between the two given input captions as a float.
    We do this with a sentence transformer model, the similarity is the classic cosine similarity.
    """

    _embeddings_1 = model_sim.encode(caption1, convert_to_tensor=True)
    _embeddings_2 = model_sim.encode(caption2, convert_to_tensor=True)

    return util.cos_sim(_embeddings_1, _embeddings_2).item()


def find_closest_joke_for_topic(topic: Topic, amount_of_retruns: int = 1) -> str:
    """This function returns from the list of TAGS the one closest to the input-label
    in the latent space of our language sentence-transformer model"""

    _embed_topic = model_sim.encode(topic.value, convert_to_tensor=True)

    _list_sims_for_tags = [[util.cos_sim(_embed_topic, _embed_joke).item(), joke]
                           for _embed_joke, joke in EMBEDDED_JOKES]

    return sorted(_list_sims_for_tags, key=lambda x: x[0], reverse=True)[0][1]


closest = find_closest_joke_for_topic(Topic.SPORTS)
print(closest)
