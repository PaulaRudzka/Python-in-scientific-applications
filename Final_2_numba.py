import numpy as np
import random 
from PIL import Image
from matplotlib import cm
import numba
from numba import jit, njit
import argparse
from tqdm import tqdm
import pandas as pd

#dla domyślnych wartości liczy się 42s


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
n=args.n 
J=args.J
B=args.B
b=args.b
positive=args.positive
step=args.step
ifile=args.ifile
mfile=args.mfile
gfile=args.gfile



def ext(A):
    a=np.array(A[0,:])
    A1=np.vstack((A,a))
    b=np.array(A1[:,0])
    A2=np.c_[A1,b]
    return A2

@jit
def energy(A):
    S=0
    for i in range(n-1):
        for j in range(n-1):
            S+=A[i][j]*A[i][j+1]
            S+=A[j][i]*A[j+1][i]

    for i in range(n - 1):
        S += A[n - 1][i] * A[0][i]  # Ostatni rząd * Pierwszy rząd
        S += A[i][n - 1] * A[i][0]
    H1=-J*S
    H2=-B*np.sum(A)
    H=H1+H2
    return H

@jit
def spin(A,b,x,y):
    E1=energy(A)
    A[x][y]=-A[x][y]
    E2=energy(A)
    if E2-E1>0:
        gg=random.random()
        # print(gg)
        if gg > np.exp(-b*(E2-E1)):
            # print('nie tym razem')
            A[x][y]=-A[x][y]
            # A2[x][y]=-A2[x][y]
    return A

@jit
def magn(A2):
    a=np.sum(A2)
    return a/n**2


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
    if args.ifile is not None:
        im.save(args.ifile + str(k)+'.jpg')   


A=np.random.choice([1, -1], (args.n, args.n),(positive,1-positive))

M=[]
colors=['RED','GREEN','YELLOW']
for i in tqdm(range(step),position=0,colour='MAGENTA', ascii=' ✿✿', ncols=100):
    m=np.copy(A)
    img(m,i)
    for j in tqdm(range(n**2),position=1,leave=False, colour=colors[i%3],ascii=" ♡♡",ncols=100):
        x,y=np.random.randint(n,size=2)
        A=spin(A,b,x,y)
    mm=magn(A)
    M.append(mm)

if args.mfile is not None:
    df_o = pd.DataFrame(M)
    df_o.to_csv(args.mfile+'.csv', index=False, header=False)

if args.mfile is not None:
    data = pd.read_csv(args.mfile+'.csv', header=None)
    data.columns=['M']
    data['M'].plot()

if gfile is not None:
    l=[]
    for i in range(step):
        im=Image.open(ifile+str(i)+'.jpg')
        l.append(im)
    l[0].save(gfile+'.gif',
                save_all=True, append_images=l[1:], optimize=False, duration=500, loop=0)
