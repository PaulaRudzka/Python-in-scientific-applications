#importing libraries 
import pandas as pd
from ascii_graph import Pyasciigraph
import collections 
import collections.abc
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
import argparse
import mmap
from pathlib import Path
from tqdm import tqdm
from time import sleep
collections.Iterable = collections.abc.Iterable


#long output
pd.options.display.max_seq_items = 2000

# comma-separated split
def list_of_strings(arg):
    return arg.split(',')

# adding arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--head_number', type=int, default=10) #eg: python parse.py -l 3
parser.add_argument('-f', '--file_name', default="scar_tissue_pl.txt") #eg: python parse.py -f scar_tissue_pl.txt
parser.add_argument('-m', '--min_word', type=int, default=0) #eg: python parse.py -l 3
parser.add_argument('-i', '--ignore', type=list_of_strings, default=[])
parser.add_argument('-n', '--not_in_string', type=list_of_strings, default=[])
parser.add_argument('-y', '--in_string', type=list_of_strings, default=[])
args = parser.parse_args()

# counting lines
def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines
path = str(Path.cwd())+'\\Project1\\'+str(args.file_name)

# read file and collect words based on filters
words=[]
with open(path,'r', encoding="utf-8") as file:
    for line in tqdm(file, total=get_num_lines(path)): 
        for word in line.split():
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

# cleaning words
words = [i.strip('.,;:()?!-*&/"') for i in words]
words = [i for i in words if i]

count = pd.Series(words).value_counts().head(args.head_number)

hist_data=[]

for idx, name in enumerate(pd.Series(words).value_counts().head(args.head_number).index.tolist()): 
    number=pd.Series(words).value_counts().iloc[idx]
    hist_data.append((name,number))

#create graph
pattern = [Red, Yel, Gre]
graph = Pyasciigraph()
data = vcolor(hist_data, pattern)
for line in graph.graph('vcolor test', data):
    print(line)


