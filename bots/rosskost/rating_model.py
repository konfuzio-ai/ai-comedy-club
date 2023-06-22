
import torch
from torch import nn
from pathlib import Path
import os
from transformers import BertForSequenceClassification, AutoTokenizer


DEVICE: str = 'cuda' if torch.cuda.is_available() else 'cpu'
BASE_MODEL_NAME: str = "bert-base-cased"
STATE_DIR: str = os.path.join(Path(__file__).parent, "data")

#TODO: try out / use git lfs for state dict (~413 mb)

# load saved weights from training:
model = BertForSequenceClassification.from_pretrained(STATE_DIR)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

# define classification head to use and load pretrained bert and its tokeni


classification_head = nn.Sequential(
        (nn.Linear(768, 256)),
        nn.ReLU(),
        nn.Dropout(0.25),
        (nn.Linear(256, 1))).to(DEVICE)


def predict(input_text: str, model=model) -> int:
    inputs = tokenizer(input_text, return_tensors="pt").to(DEVICE)

    # TODO: add restriction if too many <UNK> tokens/token ID too high
    # or some way to filter out "glibberish"/non sense joke.
    # not too happy with this approach
    _count: int = 0
    for tokens in inputs["input_ids"].flatten():
        if tokens.item() > 15_000:
            _count += 1

    if _count/len(inputs["input_ids"].flatten()) > 0.5:
        return 1

    with torch.no_grad():
        pred = model(**inputs).logits
    return pred
