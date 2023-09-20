import keras_nlp
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import os
from typing import List, Optional, Any

from tensorflow import keras

from gpttrainer import LanguageModelInterface

class LoRATraining(LanguageModelInterface):
    """
    Usage:
    ```
    lora = LoRATraining(folder_path, data_path)
    lora.load_gpt2_model()
    lora.load_data()
    lora.train_model()
    lora.merge_weights()
    lora.save_model()
    lora.generate(category, mood)


    """
    def __init__(self, folder_path: str, data_path: str):

        self.folder_path: str = folder_path
        self.data_path: str = data_path
        self.model_path: str = os.path.join(folder_path, 'trained_model')
    
        # General hyperparameters
        self.BATCH_SIZE = 32
        self.NUM_BATCHES = 500
        self.EPOCHS = 1
        self.MAX_SEQUENCE_LENGTH = 128
        self.MAX_GENERATION_LENGTH = 200

        self.GPT2_PRESET = "gpt2_base_en"

        # LoRA-specific hyperparameters
        self.RANK = 4
        self.ALPHA = 32.0

        # Enable mixed precision training
        policy = keras.mixed_precision.Policy("mixed_float16")
        keras.mixed_precision.set_global_policy(policy)

    def load_gpt2_model(self):
        # This resets "peak" memory usage to "current" memory usage.
        tf.config.experimental.reset_memory_stats("GPU:0")

        # Load the original model.
        preprocessor = keras_nlp.models.GPT2CausalLMPreprocessor.from_preset(
            "gpt2_base_en",
            sequence_length=128,
        )
        self.lora_model = keras_nlp.models.GPT2CausalLM.from_preset(
            "gpt2_base_en",
            preprocessor=preprocessor,
        )

        for layer_idx in range(self.lora_model.backbone.num_layers):
            # Change query dense layer.
            decoder_layer = self.lora_model.backbone.get_layer(f"transformer_layer_{layer_idx}")
            self_attention_layer = decoder_layer._self_attention_layer

            # Change query dense layer.
            self_attention_layer._query_dense = LoraLayer(
                self_attention_layer._query_dense,
                rank=self.RANK,
                alpha=self.ALPHA,
                trainable=True,
            )

            # Change value dense layer.
            self_attention_layer._value_dense = LoraLayer(
                self_attention_layer._value_dense,
                rank=self.RANK,
                alpha=self.ALPHA,
                trainable=True,
            )
        
        # freeze all layers except the LoRA layers
        for layer in self.lora_model._flatten_layers():
            lst_of_sublayers = list(layer._flatten_layers())

            if len(lst_of_sublayers) == 1:  # "leaves of the model"
                if layer.name in ["lora_A", "lora_B"]:
                    layer.trainable = True
                else:
                    layer.trainable = False


    def load_data(self) -> None:
        """
        Loads data from csv file and creates a tf.data.Dataset.
        """
        df = pd.read_csv(self.data_path)      

        bodies: List[str] = df['body'].tolist()

        self.train_dataset = tf.data.Dataset.from_tensor_slices((bodies,))
        self.train_dataset = self.train_dataset.map(lambda body: body).batch(16).cache().prefetch(tf.data.AUTOTUNE)

    def _generate_text(self, model, input_text, max_length=200):
        return model.generate(input_text, max_length=max_length)


    def _get_optimizer_and_loss(self):
        optimizer = keras.optimizers.AdamW(
            learning_rate=5e-5,
            weight_decay=0.01,
            epsilon=1e-6,
            global_clipnorm=1.0,  # Gradient clipping.
        )
        # Exclude layernorm and bias terms from weight decay.
        optimizer.exclude_from_weight_decay(var_names=["bias"])
        optimizer.exclude_from_weight_decay(var_names=["gamma"])
        optimizer.exclude_from_weight_decay(var_names=["beta"])

        loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        return optimizer, loss

    def train_model(self):

        optimizer, loss = self._get_optimizer_and_loss()

        self.lora_model.compile(
            optimizer=optimizer,
            loss=loss,
            weighted_metrics=["accuracy"],
        )

        self.lora_model.fit(
            self.train_dataset,
            epochs=self.EPOCHS,
        )
    
    def save_model(self) -> None:
        """
        Saves the trained GPT2 language model.
        """
        tf.saved_model.save(self.lora_model, self.model_path)

    def generate(self, category: str = None, mood: str = None) -> str:

        prompt = ""

        # If category and mood are provided, add them to the prompt
        if category is not None and mood is not None:
            prompt = f"Category: {category}, Mood: {mood}, Joke: "

        # Generate text
        text = self._generate_text(self.lora_model, prompt, max_length=self.MAX_GENERATION_LENGTH)
        

        # Remove the prompt from the generated text
        text.replace(f"Category: {category}, Mood: {mood}, Joke: ", "")
        
        return text        

    def merge_weights(self):
        for layer_idx in range(self.lora_model.backbone.num_layers):
            self_attention_layer = self.lora_model.backbone.get_layer(
                f"transformer_layer_{layer_idx}"
            )._self_attention_layer

            # Merge query dense layer.
            query_lora_layer = self_attention_layer._query_dense

            A_weights = query_lora_layer.A.kernel  # (768, 1) (a, b)
            B_weights = query_lora_layer.B.kernel  # (1, 12, 64) (b, c, d)
            increment_weights = tf.einsum("ab,bcd->acd", A_weights, B_weights) * (self.ALPHA / self.RANK)
            query_lora_layer.original_layer.kernel.assign_add(increment_weights)

            # Merge value dense layer.
            value_lora_layer = self_attention_layer._value_dense

            A_weights = value_lora_layer.A.kernel  # (768, 1) (a, b)
            B_weights = value_lora_layer.B.kernel  # (1, 12, 64) (b, c, d)
            increment_weights = tf.einsum("ab,bcd->acd", A_weights, B_weights) * (self.ALPHA / self.RANK)
            value_lora_layer.original_layer.kernel.assign_add(increment_weights)


import math

class LoraLayer(keras.layers.Layer):
    def __init__(
        self,
        original_layer,
        rank=8,
        alpha=32,
        trainable=False,
        **kwargs,
    ):
        # We want to keep the name of this layer the same as the original
        # dense layer.
        original_layer_config = original_layer.get_config()
        name = original_layer_config["name"]

        kwargs.pop("name", None)

        super().__init__(name=name, trainable=trainable, **kwargs)

        self.rank = rank
        self.alpha = alpha

        self._scale = alpha / rank

        self._num_heads = original_layer_config["output_shape"][-2]
        self._hidden_dim = self._num_heads * original_layer_config["output_shape"][-1]

        # Layers.

        # Original dense layer.
        self.original_layer = original_layer
        # No matter whether we are training the model or are in inference mode,
        # this layer should be frozen.
        self.original_layer.trainable = False

        # LoRA dense layers.
        self.A = keras.layers.Dense(
            units=rank,
            use_bias=False,
            # Note: the original paper mentions that normal distribution was
            # used for initialization. However, the official LoRA implementation
            # uses "Kaiming/He Initialization".
            kernel_initializer=keras.initializers.VarianceScaling(
                scale=math.sqrt(5), mode="fan_in", distribution="uniform"
            ),
            trainable=trainable,
            name=f"lora_A",
        )
        # B has the same `equation` and `output_shape` as the original layer.
        # `equation = abc,cde->abde`, where `a`: batch size, `b`: sequence
        # length, `c`: `hidden_dim`, `d`: `num_heads`,
        # `e`: `hidden_dim//num_heads`. The only difference is that in layer `B`,
        # `c` represents `rank`.
        self.B = keras.layers.EinsumDense(
            equation=original_layer_config["equation"],
            output_shape=original_layer_config["output_shape"],
            kernel_initializer="zeros",
            trainable=trainable,
            name=f"lora_B",
        )

    def call(self, inputs):
        original_output = self.original_layer(inputs)
        if self.trainable:
            # If we are fine-tuning the model, we will add LoRA layers' output
            # to the original layer's output.
            lora_output = self.B(self.A(inputs)) * self._scale
            return original_output + lora_output

        # If we are in inference mode, we "merge" the LoRA layers' weights into
        # the original layer's weights - more on this in the text generation
        # section!
        return original_output
