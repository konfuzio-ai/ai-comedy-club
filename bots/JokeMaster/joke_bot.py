import transformers

from .torch_serve import PyTorchServer, PytorchServerConfig
from .utils import PRETRAINED_MODEL, SCALE_SYSTEM_PROMPT, JOKE_SYSTEM_PROMPT


class Bot:
    def __init__(self, bit8: bool = False):
        config = PytorchServerConfig(
            max_length=4096,
            max_new_tokens=1024,
            max_gpu_perc_to_use=0.95
        )

        server = PyTorchServer(config=config)
        load_kw = server.get_model_load_kwargs()
        if bit8:
            load_kw['load_in_8bit'] = True
        model = transformers.LlamaForCausalLM.from_pretrained(PRETRAINED_MODEL, **load_kw)
        tokenizer = transformers.LlamaTokenizerFast.from_pretrained(PRETRAINED_MODEL)

        server.model = model
        server.tokenizer = tokenizer
        self.server = server

    def tell_joke(self):
        string = self.server.format_instruct(system=JOKE_SYSTEM_PROMPT, instruction=f"Tell me a Joke")
        for response in self.server.process(
                string=string,
                max_new_tokens=1024,
                temperature=0.8,
                max_length=1024,
                top_k=50,
                top_p=0.9,
                stream=True,
                sample=True
        ):
            yield response

    def rate_joke(self, joke: str):
        string = self.server.format_instruct(system=SCALE_SYSTEM_PROMPT, instruction=f"Rate this joke :\n{joke}")
        for response in self.server.process(
                string=string,
                max_new_tokens=1024,
                temperature=0.8,
                max_length=1024,
                top_k=50,
                top_p=0.9,
                stream=True,
                sample=True
        ):
            yield response
