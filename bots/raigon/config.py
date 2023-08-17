class JokeApiConfig:
    christmas_joke_api_url = 'https://v2.jokeapi.dev/joke/Christmas?blacklistFlags=nsfw,religious,racist,sexist,explicit'
    programming_joke_api_url = 'https://v2.jokeapi.dev/joke/Programming,Christmas?blacklistFlags=nsfw,religious,racist,sexist,explicit&type=single'


class JokeModelConfig:
    path_to_joke_generator_model = 'raigon44/iTellJokes'
    path_to_joke_rater_model = 'raigon44/iRateJokes'


class JokeGeneratorModelConfig:
    task = "generation"
    model_name = "gpt2"
    output_dir = 'models/joke_gen_model/output'
    num_train_epochs = 1
    per_device_train_batch_size = 2
    per_device_eval_batch_size = 2
    save_steps = 1000
    save_total_limit = 2
    evaluation_strategy = 'epoch'
    logging_steps = 500
    learning_rate = 2e-5
    logging_dir = 'models/joke_gen_model/logs'
    report_to = "none"


class JokeRaterModelConfig:
    task = "classification"
    model_name = "bert-base-uncased"
    num_labels = 10
    output_dir = 'models/joke_rater_model/output'
    num_train_epochs = 1
    per_device_train_batch_size = 2
    per_device_eval_batch_size = 2
    save_steps = 1000
    save_total_limit = 2
    evaluation_strategy = 'epoch'
    logging_steps = 500
    learning_rate = 2e-5
    logging_dir = 'models/joke_rater_model/logs'
    report_to = "none"


class FileConfig:
    user_feedback_file = 'user_feedback.json'
    data_file_url = 'https://github.com/orionw/rJokesData/raw/master/data/train.tsv.gz'
    compressed_data_file = 'data/jokes.gz'
    uncompressed_data_file = 'data/jokes.tsv'


class PerspectiveApiConfig:
    model_version = 'v1alpha1'
    method = 'commentanalyzer'
    developer_key = 'AIzaSyAYmXtrealouOBeLTodUv7NgL34ONQb-d0'          # Add you developer key for the perspective API here


class DataSetConfig:
    train_ratio = 0.7
    test_ratio = 0.15
    val_ratio = 0.15
