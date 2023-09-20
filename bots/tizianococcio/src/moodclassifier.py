import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
import os
from tensorflow import keras
from keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.regularizers import l2

class TextClassifier:
    """
    A class used to represent a Text Classifier with Transformer blocks

    ...

    Attributes
    ----------
    maxlen : int
        Maximum length of the input sequences
    vocab_size : int
        Size of the vocabulary
    embed_dim : int
        Embedding size for each token
    num_heads : int
        Number of attention heads
    ff_dim : int
        Hidden layer size in feed forward network inside transformer

    Methods
    -------
    fit(df_emotions: pd.DataFrame, test_size: float = 0.2)
        Train the model on given text data.
    predict(text: str)
        Predict the label of a given text.

    Usage
    -----
        Training:
            classifier = TextClassifier(maxlen=200, vocab_size=20000, embed_dim=64)
            classifier.fit(df_emotions_balanced, epochs=50, batch_size=32)

        Inference:
            loaded_model = TextClassifier(maxlen=200, vocab_size=20000, embed_dim=64)
            loaded_model.load_model("models/mood_classifier_transformer/")
            loaded_model.predict("something about passion.")
    """
    
    def __init__(self, maxlen: int, vocab_size: int, embed_dim: int = 32, num_heads: int = 2, ff_dim: int = 32):
        self.maxlen = maxlen
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim # Embedding size for each token
        self.num_heads = num_heads # Number of attention heads
        self.ff_dim = ff_dim # Hidden layer size in feed forward network inside transformer
        self.tokenizer = Tokenizer(num_words=vocab_size)
        self.le = LabelEncoder()
        
    class TransformerBlock(layers.Layer):
        def __init__(self, embed_dim: int, num_heads: int, ff_dim: int, rate: float = 0.1):
            super().__init__()
            self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
            self.ffn = keras.Sequential(
                [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim)]
            )
            self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
            self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
            self.dropout1 = layers.Dropout(rate)
            self.dropout2 = layers.Dropout(rate)

        def call(self, inputs: tf.Tensor, training: bool):
            attn_output = self.att(inputs, inputs)
            attn_output = self.dropout1(attn_output, training=training)
            out1 = self.layernorm1(inputs + attn_output)
            ffn_output = self.ffn(out1)
            ffn_output = self.dropout2(ffn_output, training=training)
            return self.layernorm2(out1 + ffn_output)

    class TokenAndPositionEmbedding(layers.Layer):
        def __init__(self, maxlen: int, vocab_size: int, embed_dim: int):
            super().__init__()
            self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
            self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

        def call(self, x: tf.Tensor):
            maxlen = tf.shape(x)[-1]
            positions = tf.range(start=0, limit=maxlen, delta=1)
            positions = self.pos_emb(positions)
            x = self.token_emb(x)
            return x + positions

    def fit(self, df_emotions: pd.DataFrame, test_size: float = 0.2, epochs: int = 2, batch_size: int = 32):
        x_train, x_val, y_train, y_val = train_test_split(df_emotions['content'], df_emotions['sentiment'], test_size=test_size, stratify=df_emotions['sentiment'])

        y_train = self.le.fit_transform(y_train)
        y_val = self.le.transform(y_val)

        y_train = np.array(y_train)
        y_val = np.array(y_val)

        self.tokenizer.fit_on_texts(df_emotions['content'])

        x_train = self.tokenizer.texts_to_sequences(x_train)
        x_val = self.tokenizer.texts_to_sequences(x_val)

        x_train = keras.preprocessing.sequence.pad_sequences(x_train, maxlen=self.maxlen)
        x_val = keras.preprocessing.sequence.pad_sequences(x_val, maxlen=self.maxlen)

        inputs = layers.Input(shape=(self.maxlen,))
        embedding_layer = self.TokenAndPositionEmbedding(self.maxlen, self.vocab_size, self.embed_dim)
        x = embedding_layer(inputs)
        transformer_block = self.TransformerBlock(self.embed_dim, self.num_heads, self.ff_dim, rate=0.2)
        x = transformer_block(x)
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(20, activation="relu")(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(len(self.le.classes_), activation="softmax")(x)

        self.model = keras.Model(inputs=inputs, outputs=outputs)
        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        self.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_val, y_val))

    def predict(self, text: str):
        sequence = self.tokenizer.texts_to_sequences([text])
        sequence = keras.preprocessing.sequence.pad_sequences(sequence, maxlen=self.maxlen)
        prediction = self.model.predict(sequence)
        predicted_label = self.le.inverse_transform([np.argmax(prediction)])
        return predicted_label[0]
    
    def save_model(self, model_path: str):
        """
        Save the trained model and tokenizer to the specified paths.

        Parameters:
        model_path (str): The path where the model will be saved.
        tokenizer_path (str): The path where the tokenizer will be saved.
        """
        # Save the model
        self.model.save(os.path.join(model_path, 'model.h5'))

        # Save the tokenizer
        with open(os.path.join(model_path, 'tokenizer.pkl'), 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # Save the label encoder
        with open(os.path.join(model_path, 'label_encoder.pkl'), 'wb') as handle:
            pickle.dump(self.le, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_model(self, model_dir: str):
        """
        Load the trained model, tokenizer and labelencoder from the specified directory.

        Parameters:
        model_dir (str): The directory where the model, tokenizer, and labelencoder are stored.
        """
        # Specify the custom objects
        custom_objects = {"TokenAndPositionEmbedding": self.TokenAndPositionEmbedding, "TransformerBlock": self.TransformerBlock}
        
        # Load the model
        self.model = keras.models.load_model(os.path.join(model_dir, 'model.h5'), custom_objects=custom_objects)

        # Load the tokenizer
        with open(os.path.join(model_dir, 'tokenizer.pkl'), 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        
        # Load the label encoder
        with open(os.path.join(model_dir, 'label_encoder.pkl'), 'rb') as handle:
            self.le = pickle.load(handle)

