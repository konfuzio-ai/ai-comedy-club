from transformers import GPT2Tokenizer

BATCH_SIZE = 16
EPOCHS = 4
LEARNING_RATE = 3e-5
MAX_LEN = 64
TRAIN_PATH = "/content/drive/MyDrive/Jokes/Joke_Generation/shortjokes.csv"
MODEL_FOLDER = "/content/drive/MyDrive/Jokes"
Tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')