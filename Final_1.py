import pandas as pd
pd.options.display.max_seq_items = 2000
from ascii_graph import Pyasciigraph
import collections 
import collections.abc
collections.Iterable = collections.abc.Iterable
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
import argparse
import mmap
from tqdm import tqdm
from time import sleep
 
 

def list_of_strings(arg):
    return arg.split(',')

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--head_number', type=int, default=10) #np: python parse.py -l 3
parser.add_argument('-f', '--file_name', default="scar_tissue_eng.txt") #np: python parse.py -f scar_tissue_pl.txt
parser.add_argument('-m', '--min_word', type=int, default=0) #np: python parse.py -l 3
parser.add_argument('-i', '--ignore', type=list_of_strings, default=[])
parser.add_argument('-n', '--not_in_string', type=list_of_strings, default=[])
parser.add_argument('-y', '--in_string', type=list_of_strings, default=[])

args = parser.parse_args()


def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines



words=[]
with open(args.file_name,'r', encoding="utf-8") as file:
    # reading each line    
    # for line in file:
    for line in tqdm(file, total=get_num_lines(args.file_name)):
        # reading each word        
        for word in line.split():
            # displaying the words           
            # print(word)
            m=0
            if len(args.in_string) ==0:
                m=1
            n=0
            word=word.lower()
            if (len(word) > args.min_word) and (word not in args.ignore) :
                for i in args.in_string:
                    if i.lower() in word:
                        m+=1
                for i in args.not_in_string:
                    if i.lower() in word:
                        n+=1 
                if m>0 and n==0:
                    words.append(word)
# print(words)
# print("/n")
words = [i.strip('.,;:()?!-*&/"') for i in words]
words = [i for i in words if i]
# print(words)

count = pd.Series(words).value_counts().head(args.head_number)
# print("Element Count")
# print(count)

hist_data=[]
# hist_d=zip(count.index, count.values)
# hist_d

for idx, name in enumerate(pd.Series(words).value_counts().head(args.head_number).index.tolist()): 
    number=pd.Series(words).value_counts().iloc[idx]
    hist_data.append((name,number))

pattern = [Red, Yel, Gre]
graph = Pyasciigraph()
data = vcolor(hist_data, pattern)
for line in graph.graph('vcolor test', data):
    print(line)


