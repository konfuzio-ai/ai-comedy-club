"""
Model which powers the joke generation and judgement of MadMeme bot.

The Fuyu-8b model is released by Adept and a pretrained version is available via huggingface.
See: https://www.adept.ai/blog/fuyu-8b and https://huggingface.co/adept/fuyu-8b.
"""

import time
from typing import Optional

import numpy as np
import torch
from transformers import (
    AutoTokenizer,
    BitsAndBytesConfig,
    FuyuForCausalLM,
    FuyuImageProcessor,
    FuyuProcessor,
)

from bots.MadMeme.utils import url_to_image


class Fuyu:
    """Pretrained fuyu model of Adept via huggingface"""

    def __init__(
        self,
        model_id: str = "ybelkada/fuyu-8b-sharded",
        force_cpu: bool = False,
    ) -> None:
        supported = ["adept/fuyu-8b", "ybelkada/fuyu-8b-sharded"]
        if model_id not in supported:
            raise ValueError(f"'model_id' needs to be one of {supported}.")

        # check if GPU can be used
        if torch.cuda.is_available() and not force_cpu:
            print("You are running the model on GPU.")
            self.device = torch.device("cuda")
            self.dtype = torch.float16
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_compute_dtype=self.dtype
            )
            self.model = FuyuForCausalLM.from_pretrained(
                model_id, quantization_config=quantization_config
            )
        else:
            print(
                "You are running the model on CPU, the runtime might be very"
                " slow. 🐌"
            )
            self.device = torch.device("cpu")
            self.dtype = torch.bfloat16
            # 4bit quantization is currently not working with the latest version of transformers (as of today: 4.35.0.dev0),
            # it is working with transformers 4.30, however fuyu is not integrated there.
            self.model = FuyuForCausalLM.from_pretrained(
                model_id, device_map=self.device, torch_dtype=self.dtype
            )

        # initialize tokenizer and fuyu processor, pretrained and via huggingface
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.processor = FuyuProcessor(
            image_processor=FuyuImageProcessor(), tokenizer=self.tokenizer
        )

    def prompt(
        self,
        text: str,
        image: Optional[np.ndarray] = None,
        out_tokens: int = 50,
    ) -> str:
        """Prompt the model with a text and optional an image prompt."""

        if image is None:
            # If no image is provided, use a small image with random normal noise.
            # It will add variation in the joke generation, after fine tuning the model
            # image = np.random.normal(np.ones((60, 60, 3), dtype=np.uint8))
            # For test purpose only!
            image = np.zeros((30, 30, 3), dtype=np.uint8)

        # pre processing image and text
        inputs = self.processor(
            text=text, images=[image], return_tensors="pt"
        ).to(self.device)
        prompt_len = inputs["input_ids"].shape[-1]

        # process
        t0 = time.time()
        generation_output = self.model.generate(
            **inputs,
            max_new_tokens=out_tokens,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        print(f"\nGeneration time: {time.time()-t0:.0f}s")

        # post processing
        generation_text = self.tokenizer.decode(
            generation_output[0][prompt_len:], skip_special_tokens=True
        )
        return generation_text.lstrip()


if __name__ == "__main__":
    # test the model
    fuyu = Fuyu("adept/fuyu-8b", force_cpu=True)

    text = "Generate a coco-style caption.\n"
    img_path = "https://huggingface.co/adept/fuyu-8b/resolve/main/bus.png"

    image = url_to_image(img_path)
    output = fuyu.prompt(text, image)

    assert (
        output == "A bus parked on the side of a road."
    ), "Something went wrong. Default example is incorrect."
    print(f"\nThe model ran successfully.\n")
