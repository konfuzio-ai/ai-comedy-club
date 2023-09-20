class DataSetConfig:
    train_ratio = 0.8
    test_ratio = 0.1
    val_ratio = 0.1

class JokeTellerModelConfig:
    model_path = 'trained_models/gpt2_joker_19.pt'
    output_dir = 'trained_models'
    num_train_epochs = 5
    per_device_train_batch_size = 2
    per_device_eval_batch_size = 2
    save_steps = 1000
    save_total_limit = 2
    evaluation_strategy = 'epoch'
    logging_steps = 500
    learning_rate = 5e-3

class JokeRaterModelConfig:
    model_path = 'trained_models/gpt2_rater_model'
    num_labels = 10
    output_dir = 'trained_models'
    num_train_epochs = 5
    per_device_train_batch_size = 2
    per_device_eval_batch_size = 2
    save_steps = 1000
    save_total_limit = 2
    evaluation_strategy = 'epoch'
    logging_steps = 500
    learning_rate = 5e-3