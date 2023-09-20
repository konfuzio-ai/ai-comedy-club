##################################
# Script to fine-tune gtp2 model #
##################################

from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch
from datasets import load_dataset

# Set device
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# Load a jokes dataset, modify it and split in training and validation set
dataset_name = 20000
if dataset_name == 100:
    dataset = load_dataset("mikegarts/oa_tell_a_joke_100", split="train")
    dataset = dataset.remove_columns(["SOURCE", "METADATA", "__index_level_0__"])
else:
    dataset = load_dataset("mikegarts/oa_tell_a_joke_20000", split="train")
    dataset = dataset.remove_columns(["SOURCE", "METADATA"])
dataset = dataset.train_test_split(test_size=0.2, shuffle=True)


# Init the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained("gpt2")
model = model.to(device)

# Tokenize the dataset
def process_function(examples):
    model_inputs = tokenizer(examples["INSTRUCTION"], examples["RESPONSE"], padding=True, truncation=True)
    return model_inputs

tokenized_datasets = dataset.map(process_function, batched=True, remove_columns=["INSTRUCTION", "RESPONSE"])

# Init the data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Set the training arguments and parameters
training_args = TrainingArguments(
    output_dir="./ks-gpt2-jokes",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    evaluation_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# Train the moddel
trainer.train()

# Save the model locally
trainer.save_model()

