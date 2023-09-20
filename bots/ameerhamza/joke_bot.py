import json
import tensorflow as tf
import xgboost as xgb
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from transformers import TFAutoModel, AutoTokenizer

from utility import clean_text, create_joke, preprocess_text, START_TOKEN


class Bot:
    """A Bot class that can tell and rate jokes."""

    name = 'Ameer Hamza - The Comedy King'

    def __init__(self):
        """Initialize the bot with GPT2 model and tokenizer."""
        self.model = TFGPT2LMHeadModel.from_pretrained('gpt2-medium')
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
        special_tokens_dict = {'pad_token': 'pad'}
        self.num_added_toks = self.tokenizer.add_special_tokens(special_tokens_dict)

    def load_checkpoint(self, checkpoint_path: str):
        """Load the model checkpoint from the given path."""
        ckpt = tf.train.Checkpoint(model=self.model)
        ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=2)
        if ckpt_manager.latest_checkpoint:
            ckpt.restore(ckpt_manager.latest_checkpoint)

    def tell_joke(self) -> str:
        """Generate a joke using the GPT2 model."""
        self.load_checkpoint('Weights/GPT2_Medium')
        initial_joke = tf.expand_dims(tf.convert_to_tensor(self.tokenizer.encode(START_TOKEN)), 0)
        joke = create_joke(initial_joke, 64, self.model, self.tokenizer)
        return clean_text(joke)

    def rate_joke(self, text: str) -> float:
        """
        Rate a joke using a pretrained BERT model and XGBoost.
        Input Features = BERT embeddings + Sentiment Signals
        """
        if text == "":
            raise ValueError("Joke cannot be an empty string.")
        if not isinstance(text, str):
            raise ValueError("Joke can only be a String.")
        bert = TFAutoModel.from_pretrained('prajjwal1/bert-tiny', from_pt=True)
        tokenizer = AutoTokenizer.from_pretrained('prajjwal1/bert-tiny')
        loaded_model = xgb.Booster()
        loaded_model.load_model('Weights/XGBoost/xgboost_model.json')
        pre_processed = preprocess_text(text, tokenizer, bert)
        dtest = xgb.DMatrix(pre_processed)
        preds = loaded_model.predict(dtest)
        return int(preds[0])