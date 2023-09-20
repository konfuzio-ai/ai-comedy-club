from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM
import random

class Bot:
    name = 'Quantized LLama2'
    def __init__(self):
        #loading quantized model
        self.model_name_or_path = "TheBloke/Llama-2-13B-chat-GPTQ"
        self.model_basename = "gptq_model-4bit-128g"

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, use_fast=True)

        self.model = AutoGPTQForCausalLM.from_quantized(self.model_name_or_path,
        model_basename=self.model_basename,
        use_safetensors=True,
        trust_remote_code=True,
        device="cuda:0",
        use_triton=False,
        quantize_config=None)
        self.joke_prefixes = [
            "Tell me a pun about outer space.","Do you know any hilarious jokes about vegetables?","Can you share a pun related to software development?","Can you tell me a joke about computers?",
            "Do you know any good puns about the ocean?","Can you come up with a funny joke about time travel?","Write a short, comical story about an alien who came to Earth just to try out fast food.",
            "magine a parallel universe where gravity is optional. Describe a funny day in the life of a person living there.","Narrate a humorous event in the life of a squirrel who thinks he’s a secret agent.",
            "Write a humorous tale about a superhero whose power is turning into a rubber duck.","Describe a comical situation where a ghost is afraid of humans.",
            "What would a conversation between a smartphone and a book look like?","If coffee and tea could argue, what would they fight about?",
            "Write a dialogue between two pencils arguing about who has a better point.","What would a conversation between a refrigerator and a microwave look like?","Imagine if dogs could talk. What would a chihuahua say to a great dane at the dog park",
            "If a pizza slice were a superhero, what would be its superpowers and nemesis?","Why might a banana be a good stand-in for a phone in the world of fruits?","Explain why a tomato might consider itself the king of the salad.","tell me your most favourite joke ever."
        ]

    def tell_joke(self):
        # Choose a random prefix for the joke
        prompt = random.choice(self.joke_prefixes)
        print(f"prompt: {prompt}")
        #system message
        system_message = "Your are a comedian should be a good sport. Creativity is key. You are a performer, not a monotonous joke-telling machine. Remember, this is a friendly club, so keep all jokes appropriate and safe for work.Your jokes should be worthy of Edinburgh Fringe"
        #prompt related to llama2
        prompt_template=f'''[INST] <<SYS>>
        {system_message}
        <</SYS>>

        {prompt} [/INST]'''
        #tokenize the prompt
        input_ids = self.tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
        #generate the joke
        output = self.model.generate(inputs=input_ids, temperature=0.7, max_new_tokens=512,do_sample = True,repetition_penalty = 1.1)
        return self.tokenizer.decode(output[0]).replace(prompt_template,"").strip()
    def chat_joke_bot(self):
        # Choose a random prefix for the joke
        prompt = random.choice(self.joke_prefixes)
        print(f"you: {prompt}")
        #system message
        system_message ="Your are a comedian should be a good sport. Creativity is key. You are a performer, not a monotonous joke-telling machine. You should have sometimes some level of interactivity, asking the user about their mood, their preference for joke types, and so on.Remember, this is a friendly club, so keep all jokes appropriate and safe for work..Your jokes should be worthy of Edinburgh Fringe"
        #prompt related to llama2
        prompt_template=f'''[INST] <<SYS>>
        {system_message}
        <</SYS>>

        {prompt} [/INST]'''
        input_ids = self.tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
        #infinte loop to chat with the model
        while True:
          output = self.model.generate(inputs=input_ids, temperature=0.7, max_new_tokens=512,do_sample = True,repetition_penalty = 1.1)
          resp = self.tokenizer.decode(output[0])
          print(resp.replace(prompt_template,"").strip())
          prompt_template = resp
          intermediate_promt = input("you:  ")
          #adding instruction prompt as a continuous chat
          prompt_template = prompt_template+f"[INST] {intermediate_promt} [/INST]"
          input_ids = self.tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()

    def rate_joke(self, prompt):
        system_message = "You are a comedian should be a good sport, capable of rating other performers' jokes on a scale from 1 (not funny) to 10 (hilarious). The response from you should be always numbers from (1-10) depending on the Humor,Creativity,Diversity of Jokes. Do explain why it is funny just give me the rating number. The response should be something like Rating: 10, Rating: 1"
        prompt_template=f'''[INST] <<SYS>>
        {system_message}
        <</SYS>>

        {prompt} [/INST]'''
        input_ids = self.tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
        output = self.model.generate(inputs=input_ids, temperature=0, max_new_tokens=512,)
        return self.tokenizer.decode(output[0]).replace(prompt_template,"").strip()