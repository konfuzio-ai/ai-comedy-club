from simpletransformers.classification import ClassificationModel, ClassificationArgs
import os
import pickle
import resource
rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (4096*4, rlimit[1]))

get_file_path = lambda : os.path.split(os.path.realpath(__file__))[0]

FILE_PATH_TRAIN_RATE_JOKE = get_file_path()

def build_model(model_type = "albert", model_name = "albert-base-v2", use_cuda = False):
    """
    This function provides the model, which should be trained before usage.

    Parameters
    ----------
    model_type : string, optional
        This parameter refers to the model type of the simpletransformer.classification
        framework (more details can be found in its documentation).
        The default is "albert".
    model_name : string, optional
        This parameter specifies the model architecture and it's weights.
        Similar to model_type, we refer to the documentation of
        simpletransformer.classification for further details.
        The default is "albert-base-v2".
    use_cuda : boolean, optional
        If the use_cuda flag is True, your cuda gpu will be uses.
        Caution: Ensure, that a gpu plus the required cuda framework are available.
        Otherwise use False, which will end up in training on the cpu.
        The default is False.

    Returns
    -------
    model : simpletransformers.classification.classification_model.ClassificationModel
        The model specified by model_type and model_name.

    """
    model_args = ClassificationArgs(
        regression = True
    )
    model = ClassificationModel(model_type, model_name, use_cuda = use_cuda, args = model_args, num_labels = 1)
    return model

def train_model(model, jester_train_set, jester_val_set):
    """
    This function trains the given model on the jester training set.

    Parameters
    ----------
    model : simpletransformers.classification.classification_model.ClassificationModel
        This is the (bare) model, that we should train.
    jester_train_set : pd DataFrame
        The DataFrame containing the joke texts and ratings for the trainings set.
    jester_val_set : pd DataFrame
        The DataFrame containing the joke texts and ratings for the validation set.

    Returns
    -------
    None.

    """
    model.train_model(train_df = jester_train_set, eval_df = jester_val_set, evaluate_during_training = True)

def save_model(model, filename = "joke_model", wd = None):
    """
    This function saves the model as pickle.

    Parameters
    ----------
    model : simpletransformers.classification.classification_model.ClassificationModel
        The given model which could be technically any python object.
        Nevertheless simpletransformers.classification.classification_model.ClassificationModel is the desired type.
    filename : string, optional
        The filename of the jester ratings dataset. The default is "joke_model".
    wd : string, optional
        The working directory of the model.
        The default is FILE_PATH_TRAIN_RATE_JOKE. Which is the path of this script.
        The default is indicated by None.

    Returns
    -------
    None.

    """
    pickle.dump(model, open(os.path.join(FILE_PATH_TRAIN_RATE_JOKE if wd is None else wd, "%s.pkl"%filename), "wb"))

def load_model(filename = "joke_model", wd = None):
    """
    This function loads the pickled model.

    Parameters
    ----------
    filename : string, optional
        The filename of the jester ratings dataset. The default is "joke_model".
    wd : string, optional
        The working directory of the model.
        The default is FILE_PATH_TRAIN_RATE_JOKE. Which is the path of this script.
        The default is indicated by None.

    Returns
    -------
    model : simpletransformers.classification.classification_model.ClassificationModel
        The given model which could be technically any python object.
        Nevertheless simpletransformers.classification.classification_model.ClassificationModel is the desired type.

    """
    model = pickle.load(open(os.path.join(FILE_PATH_TRAIN_RATE_JOKE if wd is None else wd, "%s.pkl"%filename), "rb"))
    return model

def rate_joke(model, joke, rating_lower_bound = 1, rating_upper_bound = 10, jester_rating_lower_bound = -9.969, jester_rating_upper_bound = 9.938):
    """
    This function rates a given joke over the given model.

    Parameters
    ----------
    model : simpletransformers.classification.classification_model.ClassificationModel
        The given model which shall be used to rate the joke.
    joke : string
        The joke, that shall be rated by the model.
    rating_lower_bound : float, optional
        The lower bound of the desired rating interval. The default is 1.
    rating_upper_bound : float, optional
        The upper bound of the desired rating interval. The default is 10.
    jester_rating_lower_bound : float, optional
        The lower bound of the jester ratings. The default is -9.969.
    jester_rating_upper_bound : float, optional
        The upper bound of the jester ratings. The default is 9.938.

    Returns
    -------
    prediction : float
        The prediction of the joke.

    """
    prediction = float(model.predict([joke])[0])
    prediction = scale_prediction(prediction, rating_lower_bound, rating_upper_bound, jester_rating_lower_bound, jester_rating_upper_bound)
    return prediction

def scale_prediction(prediction, rating_lower_bound = 1, rating_upper_bound = 10, jester_rating_lower_bound = -9.969, jester_rating_upper_bound = 9.938):
    """
    This function rescales the predicted ratings from the interval of the jester ratings.
    Parameters
    ----------
    prediction : float
        The prediction in the original jester ratings interval.
    rating_lower_bound : float, optional
        The lower bound of the desired rating interval. The default is 1.
    rating_upper_bound : float, optional
        The upper bound of the desired rating interval. The default is 10.
    jester_rating_lower_bound : float, optional
        The lower bound of the jester ratings. The default is -9.969.
    jester_rating_upper_bound : float, optional
        The upper bound of the jester ratings. The default is 9.938.

    Returns
    -------
    prediction : float
        The prediction after scaling into the desired interval.

    """
    return ((prediction - jester_rating_lower_bound) / (jester_rating_upper_bound - jester_rating_lower_bound) * (rating_upper_bound - rating_lower_bound) + rating_lower_bound)