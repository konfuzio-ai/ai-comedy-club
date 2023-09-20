from torch.utils.data import Dataset
import os
import json
import csv

class JokesDataset(Dataset):
    def __init__(self, dataset_path='dataset/'):
        super().__init__()

        jokes_path = os.path.join(dataset_path, 'shortjokes.csv')

        self.joke_list = []
        self.end_of_text_token = "<|endoftext|>"

        with open(jokes_path) as csv_file:
            csv_reader =  csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                joke_str = f"JOKE:{row[1]}{self.end_of_text_token}"
                self.joke_list.append(joke_str)

    def __len__(self):
        return len(self.joke_list)
    
    def __getitem__(self, index):
        return self.joke_list[index]