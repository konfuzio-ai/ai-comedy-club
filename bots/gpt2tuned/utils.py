import torch
from transformers import GPT2DoubleHeadsModel, GPT2Tokenizer
from datetime import datetime

model = GPT2DoubleHeadsModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
weekday = datetime.now().strftime("%A")


def generate_text(context):
    input_ids = tokenizer.encode(context, return_tensors='pt')
    outputs = model.generate(input_ids, max_length=50)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text


def answer_question(context, question):
    input_ids = tokenizer.encode(context, question, return_tensors='pt')
    outputs = model.generate(input_ids, max_length=50)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer


context = "Generate joke"
generated_text = generate_text(context)
print(generated_text)


context = input()
question = "Какая задача решается?"
answer = answer_question(context, question)
print(answer)
