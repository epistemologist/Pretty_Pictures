import numpy as np
from PIL import Image

RULE = 190
LENGTH = 300
HEIGHT = 50
LIFE_HEIGHT = 450
ITERATIONS = 2500
RULE_SET = list(map(int, bin(RULE)[2:]))
RULE_SET = [0]*(8-len(RULE_SET)) + RULE_SET
RULE_SET = RULE_SET[::-1]
init_row = [0]*LENGTH
init_row[LENGTH//2] = 1

COLORS = [[0, 0, 0], [9, 24, 51], [19, 62, 124], [10, 189, 198], [234, 0, 217], [113, 28, 145], [255, 255, 255]]

elementary_rows = [None] * (HEIGHT-1) + [init_row]
life_arr = np.zeros((LIFE_HEIGHT, LENGTH)).astype(int)
life_history = [life_arr for i in range(len(COLORS)-1)]

def update_elementary_rows():
	out = [0]
	for section in [elementary_rows[-1][i:i+3] for i in range(len(elementary_rows[-1])-2)]:
		out.append(RULE_SET[4*section[0]+2*section[1]+section[2]])
	out.append(0)
	elementary_rows.append(out)
	elementary_rows.pop(0)

def gen_next_life(arr):
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
	neighbors = neighbor_count(arr.astype(int))
	return life_vectorized(arr, neighbors)

def color_life_arr(life_states):
	image = np.amax(np.stack([(n+1)*arr for n,arr in enumerate(life_states[::-1])],axis=2),2)
	red = np.vectorize(lambda x: COLORS[x][0])
	green = np.vectorize(lambda x: COLORS[x][1])
	blue = np.vectorize(lambda x: COLORS[x][2])
	return np.stack([red(image),green(image),blue(image)],2).astype(np.uint8)

def color_elementary_arr(arr):
	color = np.vectorize(lambda x: [0,255][x])
	return np.stack([color(arr),color(arr),color(arr)],2).astype(np.uint8)

def next_image(filename):
	global life_arr
	elementary_arr = np.array([i if i!=None else [0]*LENGTH for i in elementary_rows])
	elementary_image = color_elementary_arr(elementary_arr)
	life_image = color_life_arr(life_history)
	out_image = np.concatenate([life_image, elementary_image],axis=0)
	image = Image.fromarray(out_image)
	image.save(filename+".png")
	update_elementary_rows()
	life_arr[-1] = elementary_arr[0]
	life_arr = gen_next_life(life_arr)
	life_history.append(life_arr)
	life_history.pop(0)

for i in range(ITERATIONS):
	print(i)
	next_image(str(i))
