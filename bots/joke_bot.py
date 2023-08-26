
import os   
import random
from typing import List
from pprint import pprint
import torch
import torch.nn as nn
from huggingface_hub import notebook_login
from peft import (
    PeftConfig,
    PeftModel,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)


class Bot:

    def __init__(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        PEFT_MODEL = "MohamedKhaled2000/falcon-7b-joking"

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        config = PeftConfig.from_pretrained(PEFT_MODEL)
        model = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            return_dict=True,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        self.tokenizer=AutoTokenizer.from_pretrained(config.base_model_name_or_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = PeftModel.from_pretrained(model, PEFT_MODEL)


        self.generation_config = self.model.generation_config
        self.generation_config.max_new_tokens = 200
        self.generation_config.temperature = 0.7
        self.generation_config.top_p = 0.7
        self.generation_config.num_return_sequences = 1
        self.generation_config.pad_token_id = self.tokenizer.eos_token_id
        self.generation_config.eos_token_id = self.tokenizer.eos_token_id


    def get_randomom_element(self, list:List):
        # throw an error if the list is empty
        if len(list) == 0:
            raise ValueError("List is empty")

        return list[random.randint(0, len(list) - 1)]

    def get_jokes(self, prompt:str)->List[str]:
        
        device = None
        
        if torch.cuda.is_available():
            device = torch.device("cuda")
            device_name = torch.cuda.get_device_name(device)
            print(f"CUDA Device Name: {device_name}")
        else:
            print("CUDA is not available.")    
            raise ValueError("CUDA is not available.")

        prompt = f"""
        <human>: {prompt}
        <assistant>:
        """.strip()

        encoding = self.tokenizer(prompt, return_tensors="pt").to(device)
        with torch.inference_mode():
            outputs = self.model.generate(
                input_ids = encoding.input_ids,
                attention_mask = encoding.attention_mask,
                generation_config = self.generation_config
            )

        output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        joke_lines = []
        lines = output.split('\n')

        for line in lines:
            if line.startswith("<assistant>:"):
                joke_lines.append(line[len("<assistant>: "):])


        return joke_lines
    
    def tell_joke(self,prompt:str)->str:
        jokes = self.get_jokes(prompt)
        joke = self.get_randomom_element(jokes)
        return joke
    




    def rate_joke(self, joke):

        rating=0
        return rating   