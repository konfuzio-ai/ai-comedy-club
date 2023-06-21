import csv
import re
import sys


def preparate_jokes_dataset():
    k = ""
    csv.field_size_limit(sys.maxsize)
    with open('shortjokes.csv') as f:
        spamreader = csv.reader(f, delimiter=' ', quotechar='|')
        fw = open("data.txt", "w")
        for row in spamreader:
            if spamreader.line_num == 1: continue
            row[0] = row[0].replace(re.findall(r'\d+', row[0])[0], "").replace(",", "")
            for i in row:
                k = k + i + " "
            fw.write("[JOKE] : " + k + "[EOS] \n")
            print(k)
            k = ""


preparate_jokes_dataset()
