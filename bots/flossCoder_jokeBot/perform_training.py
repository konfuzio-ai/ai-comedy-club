from aux import prepare_training_data, rename_df
from train_rate_joke import build_model, train_model, save_model

if __name__ == "__main__":
    jester_train_set, jester_test_set, jester_val_set = prepare_training_data()
    jester_train_set, jester_train_set_columns = rename_df(jester_train_set)
    jester_test_set, jester_test_set_columns = rename_df(jester_train_set)
    jester_val_set, jester_val_set_columns = rename_df(jester_train_set)
    model = build_model(use_cuda = True)
    train_model(model, jester_train_set, jester_val_set)
    save_model(model)
