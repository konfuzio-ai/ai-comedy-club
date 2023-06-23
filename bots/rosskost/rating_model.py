import os
import torch
from pathlib import Path
from transformers import AutoModelForSequenceClassification, AutoTokenizer


DEVICE: str = 'cuda' if torch.cuda.is_available() else 'cpu'
BASE_MODEL_NAME: str = "prajjwal1/bert-tiny"
STATE_DIR: str = os.path.join(Path(__file__).parent, "data", "bert_tiny")

# load saved weights from training and fitting tokenizer:
model = AutoModelForSequenceClassification.from_pretrained(STATE_DIR)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)


def predict(input_text: str, model=model) -> torch.Tensor:
    inputs = tokenizer(input_text, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        pred = model(**inputs).logits
    return pred
