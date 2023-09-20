import keras_nlp
import os
import re
from typing import List, Optional, Any
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split


from abc import ABC, abstractmethod

class LanguageModelInterface(ABC):
    """
    This is an abstract base class (ABC) that serves as an interface for language model classes.
    It enforces the implementation of the generate() method in any subclass.
    """

    @abstractmethod
    def generate(self, category: str = None, mood: str = None) -> str:
        """
        An abstract method that will generate a joke. Should be implemented by subclasses.
        """
        pass


class GPTTrainer(LanguageModelInterface):
    """
    A class for training a joke generator model.

    Attributes:
        folder_path (str): Path to the folder where model will be saved.
        data_path (str): Path to the data file.
        sequence_length (int): Sequence length for model training.
        num_epochs (int): Number of epochs for model training.
        base_model (str): Base model name.
        preprocessor (Optional[Any]): Preprocessor for base model.
        gpt2_lm (Optional[Any]): GPT2 language model.
        train_dataset (Optional[tf.data.Dataset]): Dataset for training.
        history (Optional[Any]): History of model training.
        model_path (str): Path to the saved model.
    """

    def __init__(self, folder_path: str, data_path: str, sequence_length: int = 512, num_epochs: int = 3, base_model: str = "gpt2_base_en"):
        """
        Constructs all the necessary attributes for the JokeGeneratorTrainer object.

        Args:
            folder_path (str): Path to the folder where model will be saved.
            data_path (str): Path to the data file.
            sequence_length (int, optional): Sequence length for model training. Defaults to 512.
            num_epochs (int, optional): Number of epochs for model training. Defaults to 3.
            base_model (str, optional): Base model name. Defaults to "gpt2_base_en".
        """
        # Set up mixed precision
        tf.keras.mixed_precision.set_global_policy('mixed_float16')              

        self.folder_path: str = folder_path
        self.data_path: str = data_path
        self.sequence_length: int = sequence_length
        self.num_epochs: int = num_epochs
        self.base_model: str = base_model
        self.preprocessor: Optional[Any] = None
        self.gpt2_lm: Optional[Any] = None
        self.train_dataset: Optional[tf.data.Dataset] = None
        self.history: Optional[Any] = None
        self.model_path: str = os.path.join(folder_path, 'trained_model')

    def load_data(self) -> None:
        """
        Loads data from csv file and creates a tf.data.Dataset.
        """
        df = pd.read_csv(self.data_path)      

        # Prepend "Category: {category}, Mood: {mood}, Joke: " to each body
        bodies: List[str] = ("Category: " + df['category'].astype(str) + ", Mood: " + df['Mood'].astype(str) + ", Joke: " + df['Joke']).tolist()

        # Split into train and validation sets
        train_bodies, valid_bodies = train_test_split(bodies, test_size=0.2) 

        # Prepare train and validation datasets
        self.train_dataset = tf.data.Dataset.from_tensor_slices((train_bodies,))
        self.train_dataset = self.train_dataset.batch(16).cache().prefetch(tf.data.AUTOTUNE)

        self.valid_dataset = tf.data.Dataset.from_tensor_slices((valid_bodies,))
        self.valid_dataset = self.valid_dataset.batch(16).cache().prefetch(tf.data.AUTOTUNE)

    def initialize_model(self) -> None:
        """
        Initializes the preprocessor and the GPT2 language model.
        """
        self.preprocessor = keras_nlp.models.GPT2CausalLMPreprocessor.from_preset(
            self.base_model,
            sequence_length=self.sequence_length
        )
        self.gpt2_lm = keras_nlp.models.GPT2CausalLM.from_preset(
            self.base_model, preprocessor=self.preprocessor
        )

    def train_model(self) -> None:
        """
        Compiles and trains the GPT2 language model.
        """
        learning_rate = keras.optimizers.schedules.PolynomialDecay(
            5e-5,
            decay_steps=self.train_dataset.cardinality() * self.num_epochs,
            end_learning_rate=0.0
        )
        loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        optimizer = keras.optimizers.Adam(learning_rate)

        self.gpt2_lm.compile(optimizer=optimizer, loss=loss, weighted_metrics=["accuracy"])

        callback = StopEarlyCallback(target_accuracy=0.95)  # Stop training when accuracy reaches 95%
        self.history = self.gpt2_lm.fit(self.train_dataset, validation_data=self.valid_dataset, epochs=self.num_epochs, callbacks=[callback])

    def save_model(self) -> None:
        """
        Saves the trained GPT2 language model.
        """
        tf.saved_model.save(self.gpt2_lm, self.model_path)

    def train(self) -> None:
        """
        Trains the GPT2 language model.
        """
        self.load_data()
        self.initialize_model()
        self.train_model()

    def train_and_save(self) -> None:
        """
        Trains the GPT2 language model and saves it.
        """
        self.load_data()
        self.initialize_model()
        self.train_model()
        self.save_model()

    def load_model(self) -> None:
        """
        Loads the saved GPT2 language model.
        """
        # Load the saved model
        loaded_model = tf.saved_model.load(self.model_path)
        self.initialize_model()
        self.gpt2_lm.set_weights(loaded_model.variables)

    def generate(self, category: str = None, mood: str = None) -> str:
        """
        Generates joke text using the GPT2 language model.
        If both a category and a mood are provided, the model will generate a joke with the 
        given category and mood.

        Args:
            category (str, optional): Category of the joke. Defaults to None.
            mood (str, optional): Mood of the joke. Defaults to None.

        Returns:
            Generated text.
        """
        if self.gpt2_lm is None:
          self.load_model()

        prompt = ""

        # If category and mood are provided, add them to the prompt
        if category is not None and mood is not None:
            prompt = f"Category: {category}, Mood: {mood}, Joke: "

        
        success = False

        while not success:
            try:
                # Generate text
                text = self.gpt2_lm.generate(prompt)
                text = re.sub(r'^\W+', '', text)
                success = True
            except UnicodeDecodeError:
                continue        

        # Remove the prompt from the generated text
        text = text.replace(f"Category: {category}, Mood: {mood}, Joke: ", "")
        
        return text


class StopEarlyCallback(tf.keras.callbacks.Callback):
    """
    A class used as a callback in model training. Stops training when target accuracy is reached.

    Attributes:
        target_accuracy (float): Target accuracy for stopping the training.
    """

    def __init__(self, target_accuracy: float, **kwargs):
        """
        Constructs all the necessary attributes for the StopEarlyCallback object.

        Args:
            target_accuracy (float): Target accuracy for stopping the training.
        """
        super().__init__(**kwargs)
        self.target_accuracy = target_accuracy

    def on_epoch_end(self, epoch: int, logs: Optional[dict] = None) -> None:
        """
        Called at the end of an epoch during training. Stops training if current accuracy is greater than or equal to the target accuracy.

        Args:
            epoch (int): Current epoch number.
            logs (dict, optional): Metric results for this training epoch, and for the validation epoch if validation is performed.
        """
        current_accuracy = logs.get('accuracy')
        if current_accuracy >= self.target_accuracy:
            self.model.stop_training = True
