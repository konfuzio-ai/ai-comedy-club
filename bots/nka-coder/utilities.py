import json
import pandas as pd
from joke_bot import category, processing

def format_long_memory_json():
    bot_path = 'bots/nka-coder/'
    with open(bot_path+"long_memory.json") as json_long_memory:
        long_memory = json.load(json_long_memory)
    i=0
    keys = [k for k in long_memory.keys()]
    for key in keys:
        if key[-1] not in ['.','?','!',')']:
            long_memory[key+'.'] = long_memory[key]
            del long_memory[key]

        i+=1
    json_object = json.dumps(long_memory , indent=4)
    with open(bot_path+"long_memory.json", "w") as file:
        file.write(json_object)

    print(i)

def load_long_memory():
    df = pd.read_csv('bots/nka-coder/joke_dataset.csv')
    long_memory ={}
    data = df.loc[df['humor'] == True]
    for text in data.text.values:
        long_memory[text] = {
                                "score" : 5, 
                                "category": category(processing(text)),
                                "initial score": False,
                                "processed_joke": processing(text)
                                }
    json_object = json.dumps(long_memory , indent=4)
    with open("bots/nka-coder/long_memory.json", "w") as file:
        file.write(json_object)  

    print("Finish loading long memory!!!")


def load_training_data():
    data = pd.read_csv('bots/nka-coder/joke_dataset.csv')
    one = []
    zero = []
    i=0
    for index, row in data.iterrows():
        if row['humor']==True and len(one)<51:
            one.append(processing(row['text']))
            print(row['text'])
        if row['humor']==False and len(zero)<51:
            zero.append(processing(row['text']))
    training_data = {"1": one, "0":zero}

    json_object = json.dumps(training_data, indent=4)
    with open("bots/nka-coder/training_data.json", "w") as file:
        file.write(json_object)  


    print("Finish loading training data!!!")



if __name__ == '__main__':
    load_long_memory()
    #load_training_data()