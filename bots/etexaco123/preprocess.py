import json
import torch
from urllib import request
import re

from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments


# Load your JSON jokes data
# jokes_data_file = "path/to/your/jokes_data.json"
# url = "https://raw.githubusercontent.com/taivop/joke-dataset/master/wocka.json"

# r  = request.urlopen(url)
# print(r.getcode())
# data = r.read()
# jokes_remote = json.loads(data)

# class Joke:
#     def __init__(self, category, body) -> None:
#         self.category = category
#         self.body = body

# jokes_local = []
# # print(jokeData)
# for j in jokes_remote:
#     if(j["category"]== "Blond" or j["category"]== "Puns" or j["category"]== "Knock-Knock" or j["category"]== "Lightbulb" or j["category"]== "Lawyer" or j["category"]== "Animal" or j["category"]== "Tech" ):
#         category = j["category"]
#         body = re.sub(r'-{2,}|\\{3,}|\n{2,}|\r{2,}|(\r\n){2,}| {2,}|\*{2,}|\.{2,} |\u00e2\u0080\u00aa16\.\u00e2\u0080\u00ac{1,}|_{2,}', '', j["body"])
#         # id = j["id"]
#         joke = Joke(category, body)
#         jokes_local.append(joke)

# my_jokes = [jk.__dict__ for jk in jokes_local]

# # write to a json file
# with open('./ai-comedy-club/bots/data/jokeData.json', 'w') as f:
#     json.dump(my_jokes, f, indent=4)


# Load the GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Load and preprocess your JSON jokes data
jokes_by_category = {}
jokeData = r"./ai-comedy-club/bots/data/jokeData.json"
with open(jokeData, "r") as json_file:
    jokes_data = json.load(json_file)
    for joke_entry in jokes_data:
        category = joke_entry["category"]
        joke = joke_entry["body"]
        if category not in jokes_by_category:
            jokes_by_category[category] = []
        jokes_by_category[category].append(joke)

# print(jokes_by_category)

# Fine-tuning for each category
for category, jokes in jokes_by_category.items():
    preprocessed_jokes_file = f'''./ai-comedy-club/bots/data/preprocessed_{category}_jokes.txt'''
    with open(preprocessed_jokes_file, "w", encoding="utf-8") as jokes_file:
        for joke in jokes:
            jokes_file.write(joke + "\n")

    # Load your fine-tuning data for this category
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=preprocessed_jokes_file,
        block_size=128  # Adjust the block size based on your data and available memory
    )

    # Initialize data collator
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Set up fine-tuning arguments
    training_args = TrainingArguments(
        output_dir=f"./ai-comedy-club/bots/models/output_{category}",  # Specify your output directory
        overwrite_output_dir=True,
        num_train_epochs=5.0,      # Adjust the number of epochs
        per_device_train_batch_size=8,
        save_total_limit=2,
        logging_dir=f"./ai-comedy-club/bots/logs/logs_{category}",   # Specify your logging directory
        logging_steps=500,
        learning_rate=1e-4,     # Adjust the learning rate
        evaluation_strategy="steps",
        # eval_steps=500,
        save_strategy="steps",
        save_steps=500,
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    # Fine-tune the model for this category
    trainer.train()

    # Saving model
    # trainer.save_model(f"./ai-comedy-club/bots/models/output_{category}")
