import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from typing import List, Union
from pandas import DataFrame

class TwoHundredKJokesProcessor:
    """
    Class to process jokes data for training a machine learning model.
    """
    
    def __init__(self, data_file: str) -> None:
        """
        Constructor method. Initializes the dataframe with data from the given JSON file.
        """
        self.df = pd.read_json(data_file)

    def preprocess_text(self, text: str) -> str:
        """
        Cleans the given text by replacing newline and carriage return characters with spaces,
        and reducing multiple spaces to single spaces.
        """
        return re.sub(r' {2,}', ' ', (re.sub(r'\n|\r', ' ', text)))

    def pipeline(self, filter_categories: List[str] = []) -> None:
        """
        Processes the dataframe by removing unnecessary columns, scaling the 'rating' column,
        removing specific categories, cleaning the 'body' column and removing rows where the 'body'
        column is 'nan' or has a trimmed length of 0.
        """
        if 'id' in self.df.columns:
            # Remove the id column, not necessary for training
            self.df.drop('id', axis='columns', inplace=True)

        if 'title' in self.df.columns:
            self.df.drop('title', axis='columns', inplace=True)

        # Create a MinMaxScaler object
        scaler = MinMaxScaler(feature_range=(0, 1))

        if 'rating' in self.df.columns:
            # Scale the rating values in range [0,1] using MinMaxScaler directly on the dataframe column
            self.df['rating'] = scaler.fit_transform(self.df[['rating']])
            # Rename the column to 'Rating' to match the other datasets
            self.df.rename(columns={'rating': 'Rating'}, inplace=True)

        # remove jokes of category
        for category in filter_categories:
            self.df = self.df[self.df['category'] != category]

        # sanitize text
        self.df["body"] = self.df.apply(lambda row: self.preprocess_text(row["body"]), axis=1)

        # drop 'nan' jokes
        self.df = self.df[self.df['body'].isna() == False]

        # remove rows where 'body' has a trimmed length of 0
        self.df = self.df[self.df['body'].str.strip().str.len() > 0]

        # rename 'body' column to 'Joke'
        self.df.rename(columns={'body': 'Joke'}, inplace=True)

    def balance_categories(self) -> None:
        """
        Balances the categories in the dataframe by resampling.
        """
        category_counts = self.df['category'].value_counts()
        plt.figure(figsize=(10, 6))  # Increase the size of the plot for better visualization
        category_counts.plot(kind='bar', color='b', alpha=0.5, label='Before balancing')

        avg_size = int(category_counts.mean())
        lst = [self.df[self.df['category'] == class_index].sample(min(len(group), avg_size), replace=False) 
            for class_index, group in self.df.groupby('category')]
        self.df = pd.concat(lst)

        # Check the new distribution
        balanced_counts = self.df['category'].value_counts()

        # You can plot again to visualize
        balanced_counts.plot(kind='bar', color='r', alpha=0.5, label='After balancing')

        plt.ylabel('Counts')
        plt.xlabel('Category')
        plt.title('Counts of rows for each category before and after balancing')
        plt.legend()  # Display the legend
        plt.show()


    def trim_length(self) -> None:
        """
        Trims the length of the jokes to a threshold length that covers 95% of jokes.
        """
        # Calculate lengths of all jokes
        lengths = self.df['Joke'].apply(lambda x: len(x.split()))

        # Determine a length that would cover 95% of jokes
        threshold_length = int(lengths.quantile(0.95))
        print(f"Length covering 95% of jokes: {threshold_length}")

        self.df = self.df[self.df['Joke'].str.len() <= threshold_length]

    def save(self, file_path: str) -> None:
        """
        Saves the processed dataframe to a CSV file.
        """
        self.df.to_csv(file_path)
