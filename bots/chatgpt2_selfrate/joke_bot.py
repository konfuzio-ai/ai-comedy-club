from transformers import AutoTokenizer, AutoModel
from transformers import pipeline
from transformers.utils import ModelOutput
import torch
import random


# From : https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output: ModelOutput,
                 attention_mask: torch.Tensor) -> torch.Tensor:

    # First element of model_output contains all token embeddings
    token_embeddings: torch.Tensor = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()  # noqa
    return (torch.sum(token_embeddings * input_mask_expanded, 1) /
            torch.clamp(input_mask_expanded.sum(1), min=1e-9))


# From : https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
def compute_normalized_emb_from_sentence(sentence: str) -> torch.Tensor:
    # Load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained(
        'sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained(
        'sentence-transformers/all-MiniLM-L6-v2')
    # Tokenize sentences
    encoded_input = tokenizer(sentence,
                              padding=True,
                              truncation=True,
                              return_tensors='pt')
    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Perform pooling
    sentence_embeddings = mean_pooling(model_output,
                                       encoded_input['attention_mask'])
    # Normalize embeddings
    sentence_embeddings = torch.nn.functional.normalize(
        sentence_embeddings, p=2, dim=1)
    return sentence_embeddings


MODEL = 'gpt2'
TASK = 'text-generation'


class Bot:

    name: str = 'Complete Sentences By GPT-2'

    def __init__(self) -> None:
        self.joke_generator = pipeline(TASK, model=MODEL)
        self.joke_prefixes = [
            "My joke is: ",
            "My best joke is: ",
            "My sarcastic joke is: ",
            "My cold joke is: ",
            "My funny joke is: ",
            "My sleepy joke is: "
        ]

    def _generate_joke(self, prefix: str, max_length: int) -> str:
        """Use the GPT-2 model to generate a text (joke) based on `prefix`.

        Args:
            prefix (str): Text prefix.
            max_length (int): Max length of the generated text.

        Returns:
            str: Text generated from the GPT-2 model.
        """
        output_dict = self.joke_generator(
            f'{prefix}',
            max_length=max_length,
            do_sample=True,
            pad_token_id=self.joke_generator.model.config.eos_token_id
        )[0]
        joke: str = output_dict['generated_text']
        return joke

    def tell_joke(self, prefix: str | None = None) -> str:
        """Use GPT-2 model to tell a joke.

        Generates 1-3 sentences text (joke) based on `prefix`. We iterate
        the text generation process until either:
            - './!/?' is found at the end of the text.
            - Max sentence formed with at least 2 './!/?' count.

        Args:
            prefix (str | None): Text prefix for the joke. If None, take a
                random one from self.joke_prefixes.

        Returns:
            str: Text generated from the GPT-2 model.
        """
        if prefix is None:
            # Choose a random prefix for the joke
            joke = random.choice(self.joke_prefixes)
        else:
            joke = prefix + (":" if prefix.find(':') == -1 else "")
        max_length = len(joke) + 25
        while True:
            joke = self._generate_joke(joke, max_length)
            max_length += 25
            if joke[-1] in ['.', '!', '?']:
                break
            if 0 < joke.count('.') + joke.count('!') + joke.count('?') >= 2:
                target_index = min([joke[::-1].find(i)
                                    for i in ['.', '!', '?']
                                    if joke[::-1].find(i) >= 0])
                joke = joke[::-1][target_index:][::-1]
                break
        return joke

    def rate_joke(self, joke: str) -> float:
        """Rate the generated joke with another self-generated joke.

        Rating is based on the cosine similarity between the embedddings
        of the joke with another self-generated joke with the same prefix.

        Args:
            joke (str): Text generated from the GPT-2 model.

        Returns:
            float: Rating in terms of cosine similarity [0...10].
        """
        # 1. Compute normalize embeddings from `joke`.
        emb1 = compute_normalized_emb_from_sentence(joke)  # 1,D
        # 2. Compute normalize embeddings from regenerated `joke`.
        joke2 = self.tell_joke(prefix=joke[:joke.find(':')])
        emb2 = compute_normalized_emb_from_sentence(joke2)  # 1,D
        rating: float = torch.nn.CosineSimilarity(dim=1)(emb1, emb2).item()
        return rating * 10.0
