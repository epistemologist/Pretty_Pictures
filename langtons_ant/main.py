import numpy as np
from collections import namedtuple
from PIL import Image
from tqdm import tqdm


class Grid: 
    def __init__(self, size, pad_size=None):
        if size % 2 != 1:
            raise ValueError("size must be odd!")
        # board is a numpy array where the center of the array represents the origin of \mathbb{Z}^2
        self.board = np.zeros((size,size)).astype(np.uint8)
        self.center = ((size-1)//2, (size-1)//2)
        self.pad_size = pad_size
    def __getitem__(self, key):
        try:
            dx,dy = key
            x,y = self.center
            if min(x+dx, y+dy) < 0: raise ValueError()
            return self.board[(x+dx, y+dy)]
        except IndexError: # coord too positive
            self.pad(key)
            return self.__getitem__(key)
        except ValueError: # coord too negative
            x1,y1 = self.center
            x2,y2 = key
            pad_pt = (2*x1-x2, 2*y1-y2)
            self.pad(pad_pt)
            return self.__getitem__(key)
    def __setitem__(self, key, value):
        try:
            dx, dy = key
            x,y = self.center
            if min(x+dx, y+dy) < 0: raise ValueError()
            self.board[(x+dx, y+dy)] = value
        except IndexError: # coord too big
            self.pad(key)
            self.__setitem__(key, value)
        except ValueError: # coord too small
            x1,y1 = self.center
            x2,y2 = key
            pad_pt = (2*x1-x2, 2*y1-y2)
            self.pad(pad_pt)
            return self.__setitem__(key)
    def pad(self, invalid_pos, size = None):
        x,y = self.center
        dx, dy = invalid_pos
        if size:
            self.board = np.pad(self.board, size)
        if self.pad_size:
            self.board = np.pad(self.board, self.pad_size)
        else:
            new_arr_size = max(x+dx, y+dy)+1
            if new_arr_size % 2 == 0: new_arr_size += 1
            size_delta = abs(new_arr_size - len(self.board))
            self.board = np.pad(self.board, size_delta//2)
        print(self.board.shape)
        self.center = ((len(self.board)-1)//2, (len(self.board)-1)//2)

class Ant:
    def __init__(self):
        self.pos = (0,0) # Cartesian coordinate
        self.heading = 0 # 0 for North, 1 for East, 2 for South, 3 for West
    def step(self):
        x,y = self.pos
        self.pos = [(x,y+1), (x+1,y), (x,y-1), (x-1,y)][self.heading]
    def turn(self, amount):
        self.heading += amount
        self.heading %= 4




board = Grid(201,pad_size=25)
ant = Ant()
for i in tqdm(range(25000)):
    #print(i, ant.pos, board.board.shape)
    current_square = board[ant.pos]
    if board[ant.pos] == 0:# White square
        ant.turn(1)
        board[ant.pos] = 0 if current_square else 1
        ant.step()
    else: # Black square
        ant.turn(-1)
        board[ant.pos] = 0 if current_square else 1
        ant.step()
    im = Image.fromarray(255*board.board)
    im.save(f"tmp/{i}.png")