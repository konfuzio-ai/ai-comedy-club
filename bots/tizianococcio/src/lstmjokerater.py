
from typing import Optional, Tuple, Any
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import Sequential, Model, load_model
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from src.rater import JokeRaterInterface
import pandas as pd
import pickle
import os


class LSTMJokeRater(JokeRaterInterface):
    """
    A class to create, train and use a LSTM model to rate jokes.

    Attributes:
        df (pd.DataFrame): DataFrame containing jokes and their ratings.
        max_length (Optional[int]): Maximum length of sequence.
        tokenizer (Tokenizer): Tokenizer to process text.
        model (Optional[Model]): Trained LSTM model.
        X (Any): Padded sequences of tokenized jokes.
        y (Any): Corresponding ratings of the jokes.
    """

    def __init__(self, jokes_rating_df: Optional[pd.DataFrame] = None, max_length: Optional[int] = None, model_path: Optional[str] = None, tokenizer_path: Optional[str] = None):
        """
        Initialize the LSTMJokeRater object.

        Args:
            jokes_rating_df (pd.DataFrame): DataFrame containing jokes and their ratings.
            max_length (Optional[int], optional): Maximum length of sequence. Defaults to None.
            model_path (Optional[str], optional): Path to save/load the model. Defaults to None.
            tokenizer_path (Optional[str], optional): Path to save/load the tokenizer. Defaults to None.
        """
        self.df = jokes_rating_df
        self.max_length = max_length
        self.tokenizer = Tokenizer()

        if model_path and tokenizer_path and os.path.exists(model_path) and os.path.exists(tokenizer_path):
            print(f"Loading model from {model_path}")
            self.load_model(model_path, tokenizer_path)
        else:
            self.model = None

    def preprocess_data(self) -> None:
        """
        Preprocesses the joke data by fitting a tokenizer and converting jokes to padded sequences.
        """
        # Fit a tokenizer on the jokes
        self.tokenizer.fit_on_texts(self.df['Joke'].values)

        # Convert jokes to sequences
        sequences = self.tokenizer.texts_to_sequences(self.df['Joke'].values)

        # Pad sequences so they're all the same length
        self.X = pad_sequences(sequences, maxlen=self.max_length)

        # Prepare target variable
        self.y = self.df['Rating'].values

    def train_model(self, units: int = 128, batch_size: int = 128, epochs: int = 10, save_freq: int = 10) -> Optional[Any]:
        """
        Trains a LSTM model on the preprocessed joke data.

        Args:
            units (int, optional): Number of LSTM units. Defaults to 128.
            batch_size (int, optional): Batch size for training. Defaults to 128.
            epochs (int, optional): Number of epochs to train. Defaults to 10.
            save_freq (int, optional): Frequency (in number of batches) at which to save the model. Defaults to 10.

        Returns:
            Optional[Any]: History of model training, or None if model is already trained.
        """
        if not self.model:
            # Define model
            self.model = Sequential()
            self.model.add(Embedding(input_dim=len(self.tokenizer.word_index) + 1, output_dim=100, input_length=self.X.shape[1]))
            self.model.add(LSTM(units))
            self.model.add(Dense(1, activation='sigmoid'))

            # Compile model
            self.model.compile(optimizer='adam', loss='mean_squared_error')

            # Define ModelCheckpoint callback
            checkpoint = ModelCheckpoint('models/model_{epoch:02d}_{batch:02d}.h5', save_freq=save_freq*batch_size)

            # Fit model
            self.history = self.model.fit(self.X, self.y, validation_split=0.2, batch_size=batch_size, epochs=epochs, callbacks=[checkpoint])
            return self.history
        print("Model already trained")

    def save_model(self, model_file: str, tokenizer_file: str) -> None:
        """
        Saves the LSTM model and tokenizer to files.

        Args:
            model_file (str): File to save the model.
            tokenizer_file (str): File to save the tokenizer.
        """
        # Save the model
        self.model.save(model_file)

        # Save the tokenizer
        with open(tokenizer_file, 'wb') as f:
            pickle.dump(self.tokenizer, f)

    def load_model(self, model_file: str, tokenizer_file: str) -> Tuple[Model, Tokenizer]:
        """
        Loads the LSTM model and tokenizer from files.

        Args:
            model_file (str): File to load the model.
            tokenizer_file (str): File to load the tokenizer.

        Returns:
            Tuple[Model, Tokenizer]: Loaded model and tokenizer.
        """
        # Load the model
        self.model = load_model(model_file)

        # Load the tokenizer
        with open(tokenizer_file, 'rb') as f:
            self.tokenizer = pickle.load(f)

        return self.model, self.tokenizer

    def rate_joke(self, joke: str) -> int:
        """
        Rates a joke using the LSTM model.

        Args:
            joke (str): Joke to rate.

        Returns:
            int: Rating of the joke.
        """
        # Tokenize the joke
        sequence = self.tokenizer.texts_to_sequences([joke])

        # Pad the sequence
        if hasattr(self, 'X'):
            padded_sequence = pad_sequences(sequence, maxlen=self.X.shape[1])
        else:
            padded_sequence = pad_sequences(sequence, maxlen=self.max_length)

        # Make prediction
        rating = self.model.predict(padded_sequence)

        # Unscale the rating to be in range [1,10]
        rating = rating * 9 + 1

        # Truncate to integer
        return int(rating[0][0])

class LSTMJokeRaterImproved(LSTMJokeRater):
    """
    The `JokeRaterImproved` class extends `JokeRater` with the following differences and improvements:

    1. Preprocessing:
        - In `preprocess_data`, it initializes a tokenizer with additional parameters `lower=True` and `oov_token="<OOV>"`. The first one is used to transform the text into lowercase, and the second one is used to handle out-of-vocabulary words, which improves the flexibility and robustness of the model.

    2. Training:
        - In `train_model`, it includes several major changes to enhance model performance:
            - The embedding output dimension has been increased from 100 to 200, which provides a larger, richer feature space.
            - It adds a second LSTM layer with `return_sequences=True` which means that it returns the full sequence output, not just the output at the final timestep. This helps to capture the relationships in the input sequence.
            - It includes `Dropout` layers after each LSTM layer to help prevent overfitting.
            - The activation function in the Dense layer is changed from `sigmoid` to `relu`, this provides a linear output which can be beneficial for regression tasks.
            - The loss function has been changed from 'mean_squared_error' to 'huber' loss. Huber loss is less sensitive to outliers in data than the mean squared error loss. It combines the best properties of Mean squared error loss and Mean absolute error loss.

    3. Callbacks:
        - In addition to the ModelCheckpoint callback which was present in the base `JokeRater` class, it adds two new callbacks for better model control during training:
            - `EarlyStopping` with `monitor='val_loss'` and `patience=3`. This stops training when a monitored quantity has stopped improving.
            - `ReduceLROnPlateau` with `monitor='val_loss'`, `factor=0.2`, `patience=2`, and `min_lr=0.001`. It reduces learning rate when a metric has stopped improving. This helps to find the optimal learning rate, as a smaller learning rate can enable the model to learn more fine-grained details.
    """
    def preprocess_data(self) -> None:
        """
        Preprocesses the joke data by initializing a tokenizer with specific parameters and fitting it on the data.
        """
        # Initialize a tokenizer with more parameters
        self.tokenizer = Tokenizer(lower=True, oov_token="<OOV>")
        super().preprocess_data()

    def train_model(self, units: int = 128, batch_size: int = 128, epochs: int = 10, save_freq: int = 10) -> Optional[Any]:
        """
        Trains a LSTM model on the preprocessed joke data.

        Args:
            units (int, optional): Number of LSTM units. Defaults to 128.
            batch_size (int, optional): Batch size for training. Defaults to 128.
            epochs (int, optional): Number of epochs to train. Defaults to 10.
            save_freq (int, optional): Frequency (in number of batches) at which to save the model. Defaults to 10.

        Returns:
            Optional[Any]: History of model training, or None if model is already trained.
        """
        if not self.model:
            # Define model
            self.model = Sequential()
            self.model.add(Embedding(input_dim=len(self.tokenizer.word_index) + 1, output_dim=200, input_length=self.X.shape[1]))
            self.model.add(LSTM(units, return_sequences=True))
            self.model.add(Dropout(0.2))
            self.model.add(LSTM(units))
            self.model.add(Dropout(0.2))
            self.model.add(Dense(1, activation='relu'))

            # Compile model
            self.model.compile(optimizer='adam', loss='huber')

            # Define callbacks
            checkpoint = ModelCheckpoint('models/model_{epoch:02d}_{batch:02d}.h5', save_freq=save_freq*batch_size)
            early_stopping = EarlyStopping(monitor='loss', patience=3)
            reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=2, min_lr=0.001)

            # Fit model
            self.history = self.model.fit(self.X, self.y, validation_split=0.2, batch_size=batch_size, epochs=epochs, callbacks=[checkpoint, early_stopping, reduce_lr])
            return self.history
        print("Model already trained")

