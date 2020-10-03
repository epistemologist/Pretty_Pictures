import numpy as np

roll_down = lambda x: np.roll(x, 1, axis=0)
roll_up = lambda x: np.roll(x, -1, axis=0)
roll_right = lambda x: np.roll(x, 1, axis=1)
roll_left = lambda x: np.roll(x, -1, axis=1)

def neighbor_count(arr_in):
	arr = np.pad(arr_in,1,"constant")
	left = roll_left(arr)
	right = roll_right(arr)
	up = roll_up(arr)
	down = roll_down(arr)
	out = left+right+up+down+roll_up(left)+roll_down(left)+roll_up(right)+roll_down(right)
	return out[1:-1,1:-1]

def life(cell, neighbors):
	if cell == 0:
		if neighbors == 3: return 1
	else:
		if neighbors != 2 and neighbors !=3: return 0
	return cell
life_vectorized = np.vectorize(life)
def next_gen(arr):
	neighbors = neighbor_count(arr.astype(int))
	return life_vectorized(arr, neighbors)

#arr = np.array([[0,0,0],[1,1,1],[0,0,0]])
arr = np.zeros((1000,1000))
r_pentomino = [(500+x,500+y) for x,y in [(0,1),(0,2),(1,0),(1,1),(2,1)]]
for x,y in r_pentomino:
    arr[x][y] = True
for i in range(200):
	print(i)
	arr = next_gen(arr)
