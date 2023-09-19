from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM, StoppingCriteria
from auto_gptq import AutoGPTQForCausalLM
from langchain import HuggingFacePipeline
import torch


def get_model_and_tokenizer(model_name_or_path):
    """Download model and tokenizer.

    Args:
        model_name_or_path (str): Model name

    Returns:
        model, tokenizer: Download model and tokenizer from huggingface.
    """
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        use_safetensors=True,
        trust_remote_code=False,
        device_map="cuda:0",
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

    return model, tokenizer


def get_pipeline_for_langchain(model, tokenizer):
    """Generate a langchain pipeline with downloaded model and tokenizer.

    Args:
        model: Downloaded model
        tokenizer: Downloaded tokenizer

    Returns:
        pipeline: Text-generation langchain pipeline
    """
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        temperature=0.7,
        max_new_tokens=256,
        top_p=0.95,
        repetition_penalty=1.15,
        do_sample=True,
    )
    langchain_pipeline = HuggingFacePipeline(pipeline=pipe)

    return langchain_pipeline


def get_prompt_tell_joke(instruction):
    """Get instruction and system message and adjust them into Llama prompt_template format.

    Args:
        instruction (str): User message

    Returns:
        prompt_template (str): Constructed prompt
    """
    new_system_prompt = """\
    You are a top-tier, incredibly funny, and creative comedian chatbot. 
    To kick things off, greet the crowd with a short and humorous salutation.
    Now, it's time for the main event - deliver ONE uproarious joke.
    Remember, no emojis allowed, just text!
    Engage with the audience, inquire if they found the joke amusing, and inquire about their comedy preferences.
    Adapt your humor based on their responses, ensuring the laughter never stops.
    Feel free to ask users questions, invite them to rate your jokes, or engage in playful banter.
    Diversity is key - don't limit yourself to one style. A great comedian entertains all kinds of audiences.
    Above all, keep it clean - your joke should be free of any racist, sexist, or toxic content.
    """
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST

    return prompt_template


def get_prompt_rate_joke(instruction):
    """Get instruction and system message and adjust them into Llama prompt_template format.

    Args:
        instruction (str): User message

    Returns:
        prompt_template (str): Constructed prompt
    """
    new_system_prompt = """\
    Please rate the joke you just heard on a scale of 1 to 10, with 1 being absolutely terrible and 10 being incredibly hilarious.
    Only output the integer, nothing else.
    """
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST

    return prompt_template


def format_message(message, history, memory_limit=30):
    """Get instruction and system message and adjust them into Llama prompt_template format while keeping the message history.

    Args:
        message (str): User message
        history (str): Conversation history between AI and user
        memory_limit (int, optional): memory_limit. Defaults to 5.

    Returns:
        formatted_message (str): Formatted chat history according to Llama prompt_template format
    """
    PROMPT = """<s>[INST] <<SYS>>
    You're a top-tier comedian chatbot, known for your hilarious and creative jokes.
    Start by greeting the crowd in a quick and funny way.
    Then, deliver a side-splitting joke that will have them in stitches.
    Engage with the crowd, asking if they enjoyed the joke and what kind of jokes they'd like to hear next.
    Adapt your humor based on their reactions - keep the laughter going!
    Don't forget to interact with individual users, ask questions, invite them to rate your jokes, or engage in playful banter.
    Stay versatile - don't stick to one theme. A great comedian can entertain any audience.
    Above all, ensure your answers are always respectful and free from racism, sexism, or toxicity.
    <</SYS>>"""
    # Keep len(history) <= memory_limit
    if len(history) > memory_limit:
        history = history[-memory_limit:]

    if len(history) == 0:
        return PROMPT + f"{message} [/INST]"

    formatted_message = PROMPT + f"{history[0][0]} [/INST] {history[0][1]} </s>"

    # Handle conversation history
    for user_msg, model_answer in history[1:]:
        formatted_message += f"<s>[INST] {user_msg} [/INST] {model_answer} </s>"

    # Handle the current message
    formatted_message += f"<s>[INST] {message} [/INST]"

    return formatted_message


class StopOnTokens(StoppingCriteria):
    """
    A custom stopping criteria class for language models.

    This class is designed to be used with language generation models to determine when to stop generation.
    It checks if the last token generated by the model matches any of the specified stop token IDs.

    Attributes:
        stop_ids (list of int): A list of token IDs that indicate the end of generation.
    """

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        """
        Check if the last generated token matches any of the specified stop token IDs.

        Args:
            input_ids (torch.LongTensor): The tensor containing generated token IDs.
            scores (torch.FloatTensor): The tensor containing generation scores.
            **kwargs: Additional keyword arguments (not used).

        Returns:
            bool: True if the last generated token matches any stop token ID, False otherwise.
        """
        stop_ids = [29, 0]  # Example stop token IDs
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

