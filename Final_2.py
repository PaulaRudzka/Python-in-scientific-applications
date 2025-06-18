import numpy as np
import random 
from PIL import Image
from matplotlib import cm
import argparse
from tqdm import tqdm
import pandas as pd


def list_of_strings(arg):
    return arg.split(',')

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', type=int, default=100) #np: python parse.py -l 3
parser.add_argument('-J', '--J', type=int, default=1) #np: python parse.py -f scar_tissue_pl.txt
parser.add_argument('-B', '--B', type=int, default=0.0001) #np: python parse.py -l 3
parser.add_argument('-b', '--b', type=int, default=0.5)
parser.add_argument('-p', '--positive', type=float, default=0.5)
parser.add_argument('-s', '--step', type=int, default=100)
parser.add_argument('-i', '--ifile')
parser.add_argument('-m', '--mfile')
parser.add_argument('-g', '--gfile')

args = parser.parse_args()

print(int(args.step))

class ising:
    def __init__(self):
        self.size=args.n
        self.matrix=np.random.choice([1, -1], (args.n, args.n),(args.positive,1-args.positive))
    
    # def extend(self):
    #     a=np.array(self.matrix[0,:])
    #     self.matrix=np.vstack((self.matrix,a))
    #     b=np.array(self.matrix[:,0])    
    #     self.matrix=np.c_[self.matrix,b]
    #     return self.matrix

    def energy(self):
        self.S=0
        for i in range(self.size-1):
            for j in range(self.size-1):
                self.S+=self.matrix[i][j]*self.matrix[i][j+1]
                self.S+=self.matrix[j][i]*self.matrix[j+1][i]
        for j in range(self.size-1):   
                self.S+=self.matrix[self.size-1][j]*self.matrix[0][j]
                self.S+=self.matrix[j][self.size-1]*self.matrix[j][self.size-1]  
        self.H=(-args.J*self.S)-(args.B*np.sum(self.matrix))
        return self.H
    
    def spin(self):
        x,y=np.random.randint(self.size,size=2)
        E1=self.energy()
        self.matrix[x][y]=-self.matrix[x][y]
        E2=self.energy()
        if E2-E1>0:
            gg=random.random()
            if gg > np.exp(-args.b*(E2-E1)):
                self.matrix[x][y]=-self.matrix[x][y]
    def magn(self):
        self.M=np.sum(self.matrix)/self.size**2


def img(m,k):
    m[np.where(m==-1)]=0
    m[np.where(m==1)]=255
    im = Image.new('RGB', (n*2, n*2))
    for y in range(n):
        for x in range(n):
            kolor = (m[y][x],m[y][x], m[y][x])
            for i in range(2):
                for j in range(2):
                    im.putpixel((x * 2 + i, y * 2 + j), kolor)
    # im.show()
    if args.ifile is not None:
        im.save(args.ifile + str(k)+'.jpg')     


A=ising()

n=args.n
# m=A.matrix
M=[]
colors=['RED','GREEN','YELLOW']
for i in tqdm(range(args.step),position=0, colour='MAGENTA', ascii=' ✿✿', ncols=100):
    # print(f'{i} !!!!!!!!!!!!!!!!!!!!!!!!!!')
    m=np.copy(A.matrix)
    img(m,i)
    for j in tqdm(range(args.n**2),position=1, leave=False, colour=colors[i%3],ascii=" ♡♡",ncols=100):
        # print(A.matrix)
        A.spin()
        # print(A.matrix)
    A.magn()
    M.append(A.M)

if args.mfile is not None:
    df_o = pd.DataFrame(M)
    df_o.to_csv(args.mfile+'.csv', index=False, header=False)

if args.mfile is not None:
    data = pd.read_csv('df_o.csv', header=None)
    data.columns=['M']
    data['M'].plot()

if args.gfile is not None:
    l=[]
    for i in range(5):
        im=Image.open(args.ifile +str(i)+'.jpg')
        l.append(im)
    l[0].save(args.gfile+'.gif',
                save_all=True, append_images=l[1:], optimize=False, duration=500, loop=0)
