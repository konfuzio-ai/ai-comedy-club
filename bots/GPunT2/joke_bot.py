from transformers import AutoTokenizer, AutoModel
from transformers import pipeline
from transformers.utils import ModelOutput
import torch
import re


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
        joke = "Here is a pun:"
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
        """Rate the generated joke using GPT-2.

        Args:
            joke (str): Text generated from the GPT-2 model.

        Returns:
            float: Rating generated from the GPT-2 model [0...10].
        """
        joke = f"I would rate from 0 to 10 the joke '{joke}' as: "
        max_length = len(joke) + 2
        pattern = r"[-+]?\d*\.\d+|\d+"
        while True:
            temp = self._generate_joke(joke, max_length)
            print(temp)
            numbers = re.findall(pattern, temp)
            if len(numbers) >= 3:
                try:
                    third_number = float(numbers[2])
                    if third_number >= 0 and 10 >= third_number:
                        return int(third_number)
                    else:
                        continue
                except Exception as e:
                    print(temp, e)
                    continue
            else:
                continue
