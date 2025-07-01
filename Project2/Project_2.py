import numpy as np
import random 
from PIL import Image
from matplotlib import cm
import argparse
from tqdm import tqdm
import pandas as pd

# helper for cli args with comma-separated lists
def list_of_strings(arg):
    return arg.split(',')

# parse cli arguments
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', type=int, default=100)  # size of grid
parser.add_argument('-J', '--J', type=int, default=1)    # interaction constant
parser.add_argument('-B', '--B', type=int, default=0.0001)  # external magnetic field
parser.add_argument('-b', '--b', type=int, default=0.5)   # inverse temperature (beta)
parser.add_argument('-p', '--positive', type=float, default=0.5)  # initial prob for spin=1
parser.add_argument('-s', '--step', type=int, default=100)  # number of simulation steps
parser.add_argument('-i', '--ifile')  # image file prefix
parser.add_argument('-m', '--mfile')  # magnetization csv file
parser.add_argument('-g', '--gfile')  # gif file name
args = parser.parse_args()


class ising:
    def __init__(self):
        self.size = args.n
        # create spin matrix with 1 and -1, with given probability
        self.matrix = np.random.choice([1, -1], (args.n, args.n), (args.positive, 1 - args.positive))
    
    def energy(self):
        self.S = 0
        # calculate sum of neighbor spin products (horizontal + vertical)
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                self.S += self.matrix[i][j] * self.matrix[i][j + 1]
                self.S += self.matrix[j][i] * self.matrix[j + 1][i]
        # periodic boundary conditions for last row and column
        for j in range(self.size - 1):   
            self.S += self.matrix[self.size - 1][j] * self.matrix[0][j]
            self.S += self.matrix[j][self.size - 1] * self.matrix[j][self.size - 1]  
        self.H = (-args.J * self.S) - (args.B * np.sum(self.matrix))  # total energy
        return self.H
    
    def spin(self):
        # pick random spin to flip
        x, y = np.random.randint(self.size, size=2)
        E1 = self.energy()
        self.matrix[x][y] = -self.matrix[x][y]  # flip spin
        E2 = self.energy()
        # accept flip if energy decreases, else probabilistically accept
        if E2 - E1 > 0:
            gg = random.random()
            if gg > np.exp(-args.b * (E2 - E1)):
                self.matrix[x][y] = -self.matrix[x][y]  # revert flip
    
    def magn(self):
        # calculate magnetization
        self.M = np.sum(self.matrix) / self.size ** 2


def img(m, k):
    # convert spins to 0/255 for image
    m[np.where(m == -1)] = 0
    m[np.where(m == 1)] = 255
    im = Image.new('RGB', (n * 2, n * 2))
    for y in range(n):
        for x in range(n):
            kolor = (m[y][x], m[y][x], m[y][x])
            # draw each pixel as 2x2 block
            for i in range(2):
                for j in range(2):
                    im.putpixel((x * 2 + i, y * 2 + j), kolor)
    if args.ifile is not None:
        im.save(args.ifile + str(k) + '.jpg')     


A = ising()

n = args.n
M = []
colors = ['RED', 'GREEN', 'YELLOW']

# main simulation loop
for i in tqdm(range(args.step), position=0, colour='MAGENTA', ascii=' ✿✿', ncols=100):
    m = np.copy(A.matrix)
    img(m, i)
    # attempt spin flips n^2 times each step
    for j in tqdm(range(args.n ** 2), position=1, leave=False, colour=colors[i % 3], ascii=" ♡♡", ncols=100):
        A.spin()
    A.magn()
    M.append(A.M)

# save magnetization to csv if requested
if args.mfile is not None:
    df_o = pd.DataFrame(M)
    df_o.to_csv(args.mfile + '.csv', index=False, header=False)

# plot magnetization if csv file saved
if args.mfile is not None:
    data = pd.read_csv(args.mfile + '.csv', header=None)
    data.columns = ['M']
    data['M'].plot()

# create gif from saved images (first 5 frames)
if args.gfile is not None:
    l = []
    for i in range(5):
        im = Image.open(args.ifile + str(i) + '.jpg')
        l.append(im)
    l[0].save(args.gfile + '.gif',
              save_all=True, append_images=l[1:], optimize=False, duration=500, loop=0)
