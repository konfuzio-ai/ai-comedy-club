import torch
import os

from config import JokeTellerModelConfig

def train_joker(num_epochs,
                bot,
                optimizer,
                scheduler,
                dataset_loader,
                max_seq_len):
    start_jokes_tensor = None

    # Create a the storing folder if it dos not exist
    models_folder = "trained_models"
    if not os.path.exists(models_folder):
        os.mkdir(models_folder)
    
    bot.model.train()

    proc_seq_count = 0
    sum_loss = 0.0
    batch_count = 0

    for epoch in range(num_epochs):
        print('=' * 5 + f"EPOCH {epoch} started" + '=' * 5)
        for _, joke in enumerate(dataset_loader):
            joke_tensor = torch.tensor(bot.tokenizer.encode(joke[0])).unsqueeze(0).to(bot.torch_device)

            # Skip sample from dataset if it is longer than MAX_SEQ_LEN
            if joke_tensor.size()[1] > max_seq_len:
                continue
            
            # The first joke sequence in the sequence
            if not torch.is_tensor(start_jokes_tensor):
                start_jokes_tensor = joke_tensor
                continue
            else:
                # If the next joke does not fit in, we process the sequence and leave the last joke 
                # as the start for next sequence 
                if start_jokes_tensor.size()[1] + joke_tensor.size()[1] > max_seq_len:
                    train_jokes_tensor = start_jokes_tensor
                    start_jokes_tensor = joke_tensor
                else:
                    # Add the joke to sequence, continue and try to add more
                    start_jokes_tensor = torch.cat([start_jokes_tensor, joke_tensor[:,1:]], dim=1)
                    continue

            outputs = bot.model(train_jokes_tensor, labels=train_jokes_tensor)
            loss, _ = outputs[:2]                        
            loss.backward()
            sum_loss = sum_loss + loss.detach().data

            proc_seq_count = proc_seq_count + 1
            if proc_seq_count == JokeTellerModelConfig.per_device_train_batch_size:
                proc_seq_count = 0    
                batch_count += 1
                optimizer.step()
                scheduler.step() 
                optimizer.zero_grad()
                bot.model.zero_grad()

            if batch_count == 100:
                print(f"sum loss {sum_loss}")
                batch_count = 0
                sum_loss = 0.0
    
        # Store the model after each epoch to compare the performance of them
        torch.save(bot.model.state_dict(), os.path.join(models_folder, f"gpt2_joker_{epoch}.pt"))
