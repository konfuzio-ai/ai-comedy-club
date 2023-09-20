
# Please ensure you have install these dependenices (Python Version 3.9.17)
#pip install transformers
#pip install scikit-learn
#pip install pandas
#pip install textblob
#pip install bs4
#pip install torchvision --user
#pip install xlrd

import random
import zipfile
import joblib
import pandas as pd
import os
from transformers import BertTokenizer
from textblob import TextBlob
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression

sentiment_threshold = -0.3
joke_length_threshold = 10

class Bot:
    def __init__(self):
        self.model = None
        self.sorted_happy_jokes = pd.DataFrame()
        self.sorted_sad_jokes = pd.DataFrame()
        self.sorted_neutral_jokes = pd.DataFrame()

    def preprocess_data(self):
        # Check if the preprocessed data is cached
        if os.path.exists('preprocessed_data.pkl'):
            combined_df = joblib.load('preprocessed_data.pkl')
            self.sort_jokes(combined_df)
        else:
            # If not cached, perform data preprocessing
            combined_df = self.preprocess_jokes()
            self.sort_jokes(combined_df)
            # Cache the preprocessed data
            joblib.dump(combined_df, 'preprocessed_data.pkl')
        return combined_df


    def preprocess_jokes(self):
        # Create a list to store tokenized joke texts and polarities
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        tokenized_joke_texts = []
        cleaned_texts = []
        joke_ids = []
        polarities = []

        # Unzip joke texts and ratings data
        with zipfile.ZipFile('jester_dataset_1_joke_texts.zip', 'r') as zip_ref:
            zip_ref.extractall('joke_texts')

        with zipfile.ZipFile('jester_dataset_1_1.zip', 'r') as zip_ref:
            zip_ref.extractall('ratings_data')

        # Load the ratings data
        ratings_data = pd.read_excel('ratings_data\jester-data-1.xls', header=None)

        # Initialize an empty list to store user-joke-rating data
        user_joke_ratings = []

        for i, row in ratings_data.iterrows():
            user_id = i + 1  # Assuming user IDs start from 1

            for joke_id, rating in enumerate(row[1:], start=1):
                if not pd.isna(rating) and rating != 99.0:  # Check if the rating is not NaN and not 99.0
                    user_joke_ratings.append([user_id, joke_id, rating])

        # Create a DataFrame with the user-joke-rating data
        user_joke_ratings_df = pd.DataFrame(user_joke_ratings, columns=['User_ID', 'Joke_ID', 'Rating'])

        # Directory containing the HTML joke text files
        joke_texts_directory = 'joke_texts\jokes'

        # Iterate through the HTML files in the directory
        for filename in os.listdir(joke_texts_directory):
            if filename.endswith(".html"):
                # Extract the joke ID from the filename
                joke_id = int(filename.split('init')[1].split('.html')[0])
                joke_ids.append(joke_id)

                # Read and preprocess the joke text
                with open(os.path.join(joke_texts_directory, filename), 'r') as file:
                    joke_text = file.read()
                    soup = BeautifulSoup(joke_text, 'html.parser')
                    cleaned_text = soup.get_text()
                    cleaned_texts.append(cleaned_text)

                    # Tokenize the cleaned text
                    tokenized_text = tokenizer(cleaned_text, truncation=True, padding=True, return_tensors='pt')
                    tokenized_joke_texts.append(tokenized_text)

                    # Calculate polarity
                    analysis = TextBlob(cleaned_text)
                    polarity = analysis.sentiment.polarity
                    polarities.append(polarity)

        # Create a DataFrame for tokenized joke texts, joke IDs, and polarities
        joke_texts_df = pd.DataFrame({'Cleaned_Text': cleaned_texts, 'Tokenized_Joke_Text': tokenized_joke_texts,
                                      'Joke_ID': joke_ids, 'Polarity': polarities})

        # Merge the two DataFrames based on the common identifier 'Joke_ID'
        combined_df = pd.merge(joke_texts_df, user_joke_ratings_df, on='Joke_ID', how='inner')

        # Drop any rows with NaN ratings if needed
        combined_df = combined_df.dropna(subset=['Rating'])

        # Sort the combined DataFrame by 'Joke_ID' and 'User_ID'
        combined_df = combined_df.sort_values(by=['Joke_ID', 'User_ID'])

        # Reset the index of the sorted DataFrame
        combined_df = combined_df.reset_index(drop=True)

        # Define the transformation function
        def transform_rating(rating):
            # Map the rating from -10 to 10 to the new range 1 to 10
            new_rating = ((rating + 10) / 20.0) * 9.0 + 1
            return new_rating

        # Apply the transformation to the 'Rating' column
        combined_df['Rating'] = combined_df['Rating'].apply(transform_rating)

        # Group jokes by polarity
        combined_df = combined_df.dropna(subset=['Cleaned_Text'])
        return combined_df

    def sort_jokes(self, combined_df):
        happy_jokes = combined_df[combined_df['Polarity'] > 0]
        sad_jokes = combined_df[combined_df['Polarity'] < 0]
        neutral_jokes = combined_df[combined_df['Polarity'] == 0]

        # Sort happy jokes by user ratings
        self.sorted_happy_jokes = happy_jokes.sort_values(by='Rating', ascending=False)

        # Sort sad jokes by user ratings
        self.sorted_sad_jokes = sad_jokes.sort_values(by='Rating', ascending=False)

        # Sort happy jokes by user ratings
        self.sorted_neutral_jokes = neutral_jokes.sort_values(by='Rating', ascending=False)


    def train_model(self, combined_df):
        combined_df['Joke_Length'] = combined_df['Cleaned_Text'].apply(lambda x: len(x.split()))
        X = combined_df[['Polarity', 'Joke_Length']]
        y = combined_df['Rating']
        # Load the Linear Regression model from the .pkl file
        model = joblib.load('linear_regression_model_polarity_length.pkl')
        #model = LinearRegression()
        #model.fit(X, y)
        return model

    def tell_joke(self, category):
        if category == 'happy':
            if not self.sorted_happy_jokes.empty:
                joke = random.choice(self.sorted_happy_jokes['Cleaned_Text'].values)
                return joke
            else:
                return "Sorry, no happy jokes available."
        elif category == 'sad':
            if not self.sorted_sad_jokes.empty:
                joke = random.choice(self.sorted_sad_jokes['Cleaned_Text'].values)
                return joke
            else:
                return "Sorry, no sad jokes available."
        elif category == 'neutral':
            if not self.sorted_neutral_jokes.empty:
                joke = random.choice(self.sorted_neutral_jokes['Cleaned_Text'].values)
                return joke
            else:
                return "Sorry, no neutral jokes available."

    def rate_joke(self, joke):
        analysis = TextBlob(joke)
        sentiment_polarity = analysis.sentiment.polarity
        joke_length = len(joke.split())

        if sentiment_polarity > sentiment_threshold and joke_length > joke_length_threshold:
            user_input_df = pd.DataFrame({'Polarity': [sentiment_polarity], 'Joke_Length': [joke_length]})
            predicted_rating = self.model.predict(user_input_df)
            return predicted_rating[0]
        else:
            return 1.0  # Assign a rating of 1 for non-sensical or negative sentiment jokes

def main():
    joke_bot = Bot()
    combined_df = joke_bot.preprocess_data()
    joke_bot.model = joke_bot.train_model(combined_df)  # Pass combined_df to train_model

    while True:
        user_input = input("User: Please type joke/quit ").lower()

        if user_input == 'quit':
            break

        if 'joke' in user_input:
            bot_response = input("Bot: Would you like to hear a joke or rate one? (choose 'hear'/'rate') ").lower()

            if bot_response == 'hear':
                category = input("Bot: Great! Please choose a category (happy, sad, neutral): ").lower()
                joke = joke_bot.tell_joke(category)
                print("Bot:", joke)
            elif bot_response == 'rate':
                user_joke = input("Bot: Please enter your joke: ")
                predicted_rating = joke_bot.rate_joke(user_joke)
                print(f"Bot: Predicted Rating for your joke: {predicted_rating:.2f}")
            else:
                print("Bot: I didn't understand your choice. Please select 'hear' or 'rate'.")

        else:
            print("Bot: I can tell jokes. Just ask for one!")

if __name__ == "__main__":
    main()
