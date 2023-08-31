import json
import pandas as pd
import re
import unidecode

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

def category(text):
    category = "others"
    categories= {
                "blacks":["black", "prison", "jail"],
                "latinos":["mexican", " latin"],
                "politics":["joe biden", "obama", "trump", "politic", "president"],
                "bars":["bar", "irish", "beer"],
                "sex":["sex", "virgin", "gay", "lesbian"],
                "religion":["muslim", "christian", "prophet", "jesus", "church","pastor"]
    }
    for word in text.split(' '):
        for cat in categories.keys():
            if word in categories[cat]:
                category = cat 
                return category
    return category

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



def processing(joke):
    data = pd.DataFrame([joke], columns=['text'])
    data = case_convert(data)
    data = remove_links(data)
    data = remove_shorthands(data)
    data = remove_accents(data)
    data = remove_specials(data)
    # NLP pipeline is more efficient without the remove_stopwords() preprocessing
    #data = remove_stopwords(data)
    data = normalize_spaces(data)
    return data.text[0]

#Utilities functions

def case_convert(data):
    data.text = [i.lower() for i in data.text.values]
    return data

def remove_specials(data):
    data.text =  [re.sub(r"[^a-zA-Z]"," ",text) for text in data.text.values]
    return data

def remove_shorthands(data):
    CONTRACTION_MAP = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }
    texts = []
    for text in data.text.values:
        string = ""
        for word in text.split(" "):
            if word.strip() in list(CONTRACTION_MAP.keys()):
                string = string + " " + CONTRACTION_MAP[word]
            else:
                string = string + " " + word
        texts.append(string.strip())
    data.text = texts
    return data
                
def remove_links(data):
    texts = []
    for text in data.text.values:
        remove_https = re.sub(r'http\S+', '', text)
        remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
        texts.append(remove_com)
    data.text = texts
    return data

def remove_accents(data):
    data.text = [unidecode.unidecode(text) for text in data.text.values]
    return data

def normalize_spaces(data):
    data.text = [re.sub(r"\s+"," ",text) for text in data.text.values]
    return data

def remove_stopwords(data):
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
             'you','your', 'yours', 
             'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
             "she's", 'her', 'hers', 'herself', 'it', 'its', 'itself', 
             'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
             'who', 'whom', 'this', 'that', 'these', 'those', 'am', 
             'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
             'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 
             'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
             'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
             'through', 'during', 'before', 'after', 'above', 'below', 'to', 
             'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 
             'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 
             'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
             'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 
             'so', 'than', 'too', 'very', "'s", 'can', 'will', 'just']
    texts = []
    for text in data.text.values:
        for stopword in stopwords:
            text = text.replace(stopword, "")
        texts.append(text)
    data.text = texts
    return data




if __name__ == '__main__':
    load_long_memory()
    #load_training_data()