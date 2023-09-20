from datasets import load_dataset
import os
import math

def generate_dataset(file_location,dataset_name='jokes_data.txt'):
    """
    This function generates a dataset txt file which is used to Prompt Tune the model.
    @param file_location: specifies the path to the folder in which the dataset is saved
    @param dataset_name: specifies the name of the dataset file
    @return: returns None
    """
    if not os.path.exists(file_location):
        os.makedirs(file_location)
    # stream true in order to not unnecessarily save the dataset twice
    dataset = load_dataset("Fraser/short-jokes", split="train",streaming =True)

    with open(file_location + dataset_name, "w") as file:
        for data_point in dataset:
            processed_point = data_point['text'].replace('\n','')
            file.write(processed_point)

    return None


def get_acc_steps(sp_step,base_acc_steps,acc_doubling_rate):
    """
    Function that performs gradient accumulation scheduling
    @param sp_step: iteration count
    @param base_acc_steps: Initial accumulation value
    @param acc_doubling_rate: rate by which the accumulation is performed
    @return:
    """
    if acc_doubling_rate != 0:
        return round(base_acc_steps * math.pow(2, (sp_step / acc_doubling_rate)))
    else:
        return base_acc_steps

def scale_perplexity(_perplexity):
    """
    Scales perplexity values to a range from 0 - 10. All perplexity values > 40 are automatically 0.

    @param _perplexity: Int
        Average Perplexity of the model over a token sequence
    @return: Int
        Rating based on the provided average perplexity
    """
    if _perplexity > 40.0:
        return 0
    else:
        scaled_perp = ((_perplexity // 4) - 10) * -1
        return int(scaled_perp)



