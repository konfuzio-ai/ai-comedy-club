from typing import Optional
import openai


def get_openai_joke(config: dict, prompt: str) -> Optional[str]:
    response = openai.Completion.create(
        model=config.MODEL_ID,
        prompt=config.MODEL_CONTEXT + prompt,
        **config.MODEL_PARAMS
    )
    joke = response.choices[0].text
    # remove starting and trailing whitespace
    joke = joke.strip()
    return (joke)
