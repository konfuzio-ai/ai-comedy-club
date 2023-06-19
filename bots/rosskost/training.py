import os
from pathlib import Path

from transformers import AutoModelForSequenceClassification
import torch


BASE_MODEL_NAME: str = "bert-base-cased"
CACHE_DIR: str = "D:\model_cache"
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


if __name__ == "__main__":

    if not Path(os.path.join(CACHE_DIR)).exists():
        os.mkdir(os.path.join(CACHE_DIR))

    # important to set number of labels to 1 for regression of single numeric output
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL_NAME, num_labels=1, cache_dir=CACHE_DIR)

    # bert pooler 786

    # potentially we can set a different classification head if we want to.

    # classification_head = nn.Sequential(
    #     (nn.Linear(768, 526)),
    #     nn.Dropout(0.1),
    #     nn.Dropout(0.1),
    #     (nn.Linear(526, 258)),
    #     nn.ReLU(),
    #     nn.Dropout(0.1),
    #     (nn.Linear(258, 2)),
    #     nn.Softmax()
    # ).to(DEVICE)

    print(model)
