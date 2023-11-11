from typing import Optional, List
from pydantic import BaseModel
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
from typing import Union

PRETRAINED_MODEL = "erfanzar/LinguaMatic"

JOKE_SYSTEM_PROMPT = (
    "You are an AI designed to tell jokes and rate them. Your goal is to "
    "generate humorous and entertaining jokes, Have fun and bring laughter to the users!, do not mention"
    " Anything about this is a joke or (Sure, I'd be happy to help! Here's a joke for you) only tell the joke and make "
    "Sure that it's related to the requested topic"
)

SCALE_SYSTEM_PROMPT = (
    "You are an AI designed to rate jokes on a scale from 1 to 10. Your task is to provide an objective rating for "
    "each joke, with 1 being the lowest and 10 being the highest. Your responses should solely consist of the rating, "
    "without any additional comments. Focus on evaluating the comedic value of the jokes based "
    "on factors such as cleverness, timing, and "
    "overall entertainment factor. Let your ratings speak for themselves and bring clarity "
    "to the humor quotient of each joke."
)


def prompt_model(message: str, chat_history,
                 system_prompt: str) -> str:
    do_strip = False
    texts = [f'<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n']
    for user_input, response in chat_history:
        user_input = user_input.strip() if do_strip else user_input
        do_strip = True
        texts.append(f'{user_input} [/INST] {response.strip()} </s><s>[INST] ')
    message = message.strip() if do_strip else message
    texts.append(f'{message} [/INST]')
    return ''.join(texts)


class InstructRequest(BaseModel):
    instruction: str
    system: Optional[str] = None
    temperature: Optional[float] = None
    greedy: Optional[bool] = False


class Seafoam(Base):
    def __init__(
            self,
            *,
            primary_hue: Union[colors.Color, str] = colors.emerald,
            secondary_hue: Union[colors.Color, str] = colors.blue,
            neutral_hue: Union[colors.Color, str] = colors.gray,
            spacing_size: Union[sizes.Size, str] = sizes.spacing_md,
            radius_size: Union[sizes.Size, str] = sizes.radius_md,
            text_size: Union[sizes.Size, str] = sizes.text_lg,
            font: Union[fonts.Font, str]
            = (
                    fonts.GoogleFont("Quicksand"),
                    "ui-sans-serif",
                    "sans-serif",
            ),
            font_mono: Union[fonts.Font, str]
            = (
                    fonts.GoogleFont("IBM Plex Mono"),
                    "ui-monospace",
                    "monospace",
            ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,

        )
        super().set(
            body_background_fill="linear-gradient(90deg, *secondary_800, *neutral_900)",
            body_background_fill_dark="linear-gradient(90deg, *secondary_800, *neutral_900)",
            button_primary_background_fill="linear-gradient(90deg, *primary_300, *secondary_400)",
            button_primary_background_fill_hover="linear-gradient(90deg, *primary_200, *secondary_300)",
            button_primary_text_color="white",
            button_primary_background_fill_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            slider_color="*secondary_300",
            slider_color_dark="*secondary_400",
            block_title_text_weight="600",
            block_border_width="0px",
            block_shadow="*shadow_drop_lg",
            button_shadow="*shadow_drop_lg",
            button_large_padding="4px",
        )


seafoam = Seafoam()