import os
from transformers import pipeline
import torch

HF_CACHE = "D:\model_cache"
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

os.environ['HUGGINGFACE_HUB_CACHE'] = HF_CACHE

generator = pipeline('text-generation',
                    model='gpt2',
                    framework="pt",
                    device=DEVICE)

prompt: str = "A awsome joke about programming is: \n"

joke = generator(prompt, max_length=50, do_sample=True)[0]["generated_text"]

print(joke.replace(prompt, ""))
