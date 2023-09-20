import pandas as pd
import os
from sklearn.model_selection import train_test_split

get_file_path = lambda : os.path.split(os.path.realpath(__file__))[0]
FILE_PATH_AUX = get_file_path()

def load_jester_items(wd = None, jester_items_filename = "jester_items.csv"):
    """
    Provide the jester items from the Jester 1.7M jokes ratings dataset obtained by
    https://www.kaggle.com/datasets/vikashrajluhaniwal/jester-17m-jokes-ratings-dataset.

    Parameters
    ----------
    wd : string, optional
        The working directory of the jester dataset.
        The default is None. In this case the directory of the python script is used.
    jester_items_filename : string, optional
        The filename of the jester items dataset.
        The default is "jester_items.csv".

    Returns
    -------
    jester_items : pandas DataFrame
        The jester_items contains the columns jokeId and jokeText.

    """
    jester_items_fn = os.path.join(FILE_PATH_AUX, jester_items_filename) if wd is None else os.path.join(wd, jester_items_filename)
    try:
        jester_items = pd.read_csv(jester_items_fn)
    except:
        print("Please provide the jester items csv from kaggle")
    return jester_items

def load_jester_ratings(wd = None, jester_ratings_filename = "jester_ratings.csv"):
    """
    Provide the jester ratings from the Jester 1.7M jokes ratings dataset obtained by
    https://www.kaggle.com/datasets/vikashrajluhaniwal/jester-17m-jokes-ratings-dataset.

    Parameters
    ----------
    wd : string, optional
        The working directory of the jester dataset.
        The default is None. In this case the directory of the python script is used.
    jester_ratings_filename : string, optional
        The filename of the jester ratings dataset. The default is "jester_ratings.csv".

    Returns
    -------
    jester_ratings : pandas DataFrame
        The jester_ratings contains the columns userId, jokeId and rating [-10.0, 10.0].

    """
    jester_ratings_fn = os.path.join(FILE_PATH_AUX, jester_ratings_filename) if wd is None else os.path.join(wd, jester_ratings_filename)
    try:
        jester_ratings = pd.read_csv(jester_ratings_fn)
    except:
        print("Please provide the jester ratings csv from kaggle")
    return jester_ratings

def prepare_datasets(jester_ratings, jester_items):
    """
    This function combines inputs, such that the joke text and coresponding
    rating of an item are im a dataframe.

    Parameters
    ----------
    jester_ratings : pandas DataFrame
        The jester_ratings contains the columns userId, jokeId and rating [-10.0, 10.0].
    jester_items : pd DataFrame
        The jester jokes items assigning the joke ids to the joke texts..

    Returns
    -------
    jester_set : pd DataFrame
        The DataFrame containing the joke texts and ratings for the jester data set.

    """
    jester_set = pd.DataFrame(jester_items["jokeText"][jester_ratings["jokeId"]-1])
    jester_set = jester_set.join(pd.DataFrame(jester_ratings["rating"]))
    return jester_set

def rename_df(df, columns_names = ["text", "labels"]):
    """
    This function renames the column names of the given data frame.

    Parameters
    ----------
    df : pandas DataFrame
        The data frame whose columns names shall be changed.
    columns_names : pandas.core.indexes.base.Index or list, optional
        The new columns names of the data frame.
        Make shure, that the number of labels is equals to the number of columns
        in the data frame.
        The default is ["text", "labels"].

    Raises
    ------
    Exception
        The exception is raised in case the number of columns names differs from
        the number of columns of the given data frame.

    Returns
    -------
    df : pandas DataFrame
        The data frame after changing the columns names.
    old_columns_names : pandas.core.indexes.base.Index
        The columns names of the unchanged data frame.

    """
    old_columns_names = df.columns
    if len(old_columns_names) != len(columns_names):
        raise Exception("The number of columns = %i is not equals to the number of column_names = %i"%(len(old_columns_names), len(columns_names)))
    df.columns = columns_names
    return df, old_columns_names

def train_test_val_split(jester_set):
    """
    Perform the train-, test- and validation split on the jester set
    with ratio 80:10:10.

    Parameters
    ----------
    jester_set : pd DataFrame
        The DataFrame containing the joke texts and ratings for the jester data set.

    Returns
    -------
    jester_train_set : pandas DataFrame
        The train set of the jester set dataset.
    jester_test_set : pandas DataFrame
        The test set of the jester set dataset.
    jester_val_set : pandas DataFrame
        The validation set of the jester set dataset.

    """
    jester_train_set, jester_test_set, x, y = train_test_split(jester_set, jester_set, train_size=0.8)
    jester_test_set, jester_val_set, x, y = train_test_split(jester_test_set, jester_test_set, train_size = 0.5)
    return jester_train_set, jester_test_set, jester_val_set

def prepare_training_data(number_of_samples = None, wd = None, jester_items_filename = "jester_items.csv", jester_ratings_filename = "jester_ratings.csv"):
    """
    This function performs all actions required to prepare the data.

    Parameters
    ----------
    number_of_samples : int, optional
        The number of samples drawn from the jester dataset, in case number_of_samples
        is not None.
        The default is None.
    wd : string, optional
        The working directory of the jester dataset.
        The default is None. In this case the directory of the python script is used.
    jester_items_filename : string, optional
        The filename of the jester items dataset.
        The default is "jester_items.csv"
    jester_ratings_filename : string, optional
        The filename of the jester ratings dataset. The default is "jester_ratings.csv".".

    Returns
    -------
    jester_train_set : pd DataFrame
        The DataFrame containing the joke texts and ratings for the trainings set.
    jester_test_set : pd DataFrame
        The DataFrame containing the joke texts and ratings for the test set.
    jester_val_set : pd DataFrame
        The DataFrame containing the joke texts and ratings for the validation set.

    """
    jester_items = load_jester_items(wd, jester_items_filename)
    jester_ratings = load_jester_ratings(wd, jester_ratings_filename)
    jester_set = prepare_datasets(jester_ratings, jester_items)
    if number_of_samples is not None:
        jester_set = jester_set.sample(number_of_samples)
    jester_train_set, jester_test_set, jester_val_set = train_test_val_split(jester_set)
    return jester_train_set, jester_test_set, jester_val_set