from utils import generate_dataset,get_acc_steps
from bot import Bot
from mkultra.soft_prompt import SoftPrompt
import math
import os
from transformers import  Adafactor
import transformers
from tqdm import tqdm
import random
import torch


## All trainings Paramters
# Checkpoint interval in steps.
checkpoint_interval = 20

block_size = 700

# Evaluation interval in steps.
eval_interval = 5

# How many blocks to use for evaluation.
eval_blocks = 16

# Adafactor hyperparameters
optimizer_params = {
    # Fixed learning rate
    "lr": 1e-4,

    # 1st momentum
    "beta1": 0.0,

    # 2nd momentum decay schedule
    "decay_rate": -0.1,

    # Weight decay
    "weight_decay": 0.01,

    # Update scaling
    "scale_parameter": False,

    # Built-in LR scheduler
    "relative_step": False
}

# LR scheduler parameters
scheduler_params = {
    "num_warmup_steps": 10,
    "num_cycles": 8,
    "num_training_steps": 400
}

base_acc_steps = 16
acc_doubling_rate = 0
plateau_steps = 0
sp_step = 0
eval_loss = 100

## All administrative parameters
BASE_PATH = r'data/'
DATASET_PATH = BASE_PATH +'dataset/'
TRAINING_PATH = BASE_PATH +'training_info/'
DATASET_NAME = 'jokes_data.txt'


SEED = 424
SOFTPROMPT_NAME = "johnny"
SOFTPROMPT_PATH = BASE_PATH +'soft_prompt/'


if __name__ == "__main__":

    #check if dataset already exists
    if not os.path.isfile(DATASET_PATH + DATASET_NAME):
        generate_dataset(DATASET_PATH,DATASET_NAME)

    #init bot with new soft prompt to train
    bot = Bot(False)

    with open(DATASET_PATH + DATASET_NAME, 'r', encoding='utf-8') as data_file:
        data_text = data_file.read()

    data_tokenized = bot.tokenizer.encode(data_text)

    text_length = len(data_tokenized)
    num_blocks = math.ceil(text_length / block_size)

    print(f"Length of text: {len(data_tokenized)} tokens")
    print(f"Number of blocks: {num_blocks}, each {block_size} tokens")
    #split blocks up in order to fit model context length
    blocks = list()
    for block_num in range(num_blocks):
        start = block_num * block_size
        end = min(start + block_size, text_length)
        blocks.append(data_tokenized[start:end])

    block_order = [*range(num_blocks)]
    #start setting up training
    num_training_steps = scheduler_params['num_training_steps']

    optimizer_params['params'] = [bot.model.get_soft_params()]
    optimizer = Adafactor(**optimizer_params)
    optimizer.state['step'] = sp_step

    scheduler_params['optimizer'] = optimizer
    scheduler = transformers.get_cosine_with_hard_restarts_schedule_with_warmup(**scheduler_params)

    torch.cuda.empty_cache()
    loss_log_path = os.path.join(TRAINING_PATH, "loss_log.csv")

    if not os.path.exists(TRAINING_PATH):
        os.makedirs(TRAINING_PATH)

    if not os.path.exists(SOFTPROMPT_PATH):
        os.makedirs(SOFTPROMPT_PATH)
    bar = tqdm(total=num_training_steps)
    optimizer.state['step'] = sp_step
    evals_since_last_improvement = 0
    best_eval = float('inf')

    #shuffle training data
    eval_order = [*range(num_blocks)]
    random.seed(SEED)
    random.shuffle(eval_order)

    for session_step in range(num_training_steps):
        bot.model.train()

        acc_steps = get_acc_steps(sp_step,base_acc_steps,acc_doubling_rate)

        for i in range(acc_steps):
            idx = (sp_step * acc_steps + i) % num_blocks

            if idx == 0:
                random.shuffle(block_order)


            block = blocks[block_order[idx]]

            input_ids = torch.LongTensor(block).unsqueeze(0).cuda().detach()

            # Forward pass and optimize
            outputs = bot.model(input_ids=input_ids, labels=input_ids)
            loss = outputs.loss
            loss.backward()

            instant_loss = loss.item()

            # Sanity check batch
            if math.isnan(instant_loss):
                torch.cuda.empty_cache()
                raise KeyboardInterrupt

            # Discard tensor that was moved to GPU
            del input_ids
            torch.cuda.empty_cache()

        # Accumulate gradients
        optimizer.step()
        lr = optimizer.param_groups[0]["lr"]
        scheduler.step()
        optimizer.zero_grad()

        # Sanity check iteration
        if math.isnan(instant_loss):
            torch.cuda.empty_cache()
            raise KeyboardInterrupt

        # Evaluate model and plot loss
        if sp_step % eval_interval == 0:
            bot.model.eval()
            torch.cuda.empty_cache()
            eval_loss = 0

            # no need to generate gradients
            with torch.no_grad():
                for eval_step in range(eval_blocks):
                    block = blocks[eval_order[eval_step]]
                    input_ids = torch.LongTensor(block).unsqueeze(0).cuda().detach()
                    eval_loss += bot.model(input_ids=input_ids, labels=input_ids).loss.item()

                    # Discard tensor that was moved to GPU
                    del input_ids
                    torch.cuda.empty_cache()

            eval_loss /= eval_blocks

            with open(loss_log_path, 'a+', encoding='utf-8') as file:
                file.write(f"{sp_step},{eval_loss}\n")

            # Stop if loss has plateaued
            if plateau_steps != 0:
                if eval_loss < best_eval:
                    best_eval = eval_loss
                    evals_since_last_improvement = 0
                else:
                    evals_since_last_improvement += 1
                if evals_since_last_improvement > plateau_steps:
                    print(f"No improvement for {plateau_steps} evals")
                    break

        # Save checkpoint every so often
        if sp_step % checkpoint_interval == 0:
            sp = SoftPrompt.from_tuning_model(bot.model,
                                              {"name": SOFTPROMPT_NAME + f"-step-{sp_step}",
                                               "step": sp_step,
                                               "loss": eval_loss})
            sp.to_file(SOFTPROMPT_PATH + SOFTPROMPT_NAME+".json")

        bar.set_postfix({
            "Model Step": sp_step,
            "Eval Loss": "{el:.5f}".format(el=eval_loss),
            "Acc Steps": acc_steps,
            "LR": lr
        })
        bar.update(1)
        sp_step += 1

    # Save a checkpoint once done
    sp = SoftPrompt.from_tuning_model(bot.model,
                                      {"name": SOFTPROMPT_NAME + f"-step-{sp_step}",
                                       "step": sp_step,
                                       "loss": eval_loss})
    sp.to_file(SOFTPROMPT_PATH + SOFTPROMPT_NAME+".json")