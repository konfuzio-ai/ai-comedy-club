import pandas as pd
from pandas import DataFrame
from typing import Optional

class JesterRatingDataProcessor:
    """
    This class is for processing Jester Joke Ratings data.
    
    It can load jokes from a file, add ratings, export the data to CSV, merge ratings and return the data.
    
    Attributes:
    -----------
    jokes_file : str
        The path to the file that contains the jokes.
    jokes_df : Optional[DataFrame]
        Pandas DataFrame to store the jokes data after loading from the file.
    ratings_df : Optional[DataFrame]
        Pandas DataFrame to store the ratings data after adding it to the jokes.
    ratings_merge : Optional[DataFrame]
        Pandas DataFrame to store the merged ratings data.
    
    """    
    def __init__(self, jokes_file: str):
        """
        Initializes JesterRatingDataProcessor with the jokes file.
        
        Parameters:
        -----------
        jokes_file : str
            The path to the file that contains the jokes.
        """
        self.jokes_file = jokes_file
        self.jokes_df = None
        self.ratings_df = None
        self.ratings_merge = None

    def load_data(self) -> None:
        """
        Load the jokes from the given file.
        """
        self.jokes_df = pd.read_excel(self.jokes_file, decimal=',', header=None)
        
        # Add index column to the jokes dataframe
        self.jokes_df = self.jokes_df.reset_index().rename(columns={'index': 'Index'})

    def add_ratings(self, ratings_file: str) -> None:
        """
        Add ratings to the jokes from the given ratings file.
        
        Parameters:
        -----------
        ratings_file : str
            The path to the file that contains the ratings.
        """        
        # Load the ratings
        self.ratings_df = pd.read_excel(ratings_file, decimal=',')        
        
        # Drop column with the ratings counts
        self.ratings_df.drop(self.ratings_df.columns[0], axis=1, inplace=True)

        # Transpose to have one jokes on the rows, and ratings on columns
        self.ratings_df = self.ratings_df.T

        # Reset index and drop the old index
        self.ratings_df = self.ratings_df.reset_index(drop=True)

        # Add a new 'Index' column with new indices
        self.ratings_df['Index'] = self.ratings_df.index

        # Define a new order for the columns where 'Index' comes first
        cols = ['Index'] + [col for col in self.ratings_df if col != 'Index']

        # Reorder the columns
        self.ratings_df = self.ratings_df[cols]

        # Convert to long-format
        self.ratings_df = self.ratings_df.melt(id_vars='Index', value_name='Rating').drop(columns=['variable'])

        # Make sure that data is indeed in the range [-10, 10], if out-of-range values are found marked them as missing (99)
        self.ratings_df['Rating'] = self.ratings_df['Rating'].apply(lambda x: x if -10 <= x <= 10 else 99)

        # Remove all missing values
        self.ratings_df = self.ratings_df[self.ratings_df['Rating'] != 99]

        # Rescale ratings to the range [0,1]
        self.ratings_df['Rating'] = (self.ratings_df['Rating'] + 10) / 20
        
        if self.ratings_merge is None:
            self.ratings_merge = self.ratings_df
        else:
            self.ratings_merge = pd.concat([self.ratings_merge, self.ratings_df])

    def get_data(self) -> DataFrame:
        """
        Returns the merged DataFrame of jokes and ratings.

        Returns:
        --------
        merged_df : DataFrame
            Pandas DataFrame that contains the jokes and their corresponding ratings.
        """        
        # Left-join jokes with ratings: jokes with no ratings are discarded.
        merged_df = pd.merge(self.ratings_merge, self.jokes_df, on='Index', how='left')

        # Rename the column with the jokes text
        merged_df.rename(columns={0: 'Joke'}, inplace=True)
        
        return merged_df

    def export_data(self, jokes_csv_file: str, ratings_csv_file: str) -> None:
        """
        Exports the jokes and ratings data to CSV files.
        
        Parameters:
        -----------
        jokes_csv_file : str
            The path to the file where jokes data will be exported.
        ratings_csv_file : str
            The path to the file where ratings data will be exported.
        """        
        # Export to CSV
        self.jokes_df.to_csv(jokes_csv_file)
        self.ratings_df.to_csv(ratings_csv_file)

    def merge_ratings(self, new_ratings_file: str, output_file: str) -> DataFrame:
        """
        Merge new ratings with existing ratings and export the merged data to a CSV file.
        
        Parameters:
        -----------
        new_ratings_file : str
            The path to the file that contains new ratings.
        output_file : str
            The path to the file where the merged ratings data will be exported.
        
        Returns:
        --------
        merged_df : DataFrame
            Pandas DataFrame that contains the merged ratings data.
        """        
        # Load the new ratings
        new_ratings_df = pd.read_excel(new_ratings_file)

        # Merge the existing and new ratings
        merged_df = pd.concat([self.ratings_df, new_ratings_df], ignore_index=True, axis=1)

        # Export to CSV
        merged_df.to_csv(output_file)

        return merged_df
