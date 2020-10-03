"""
neighbors = lambda x,y: [(x-1,y-1),(x-1,y),(x-1,y+1),
						 (x,  y-1),        (x  ,y+1),
						 (x+1,y-1),(x+1,y),(x+1,y+1)]
"""
neighbors = lambda x,y: [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
def next_gen(arr):
	l, w = len(arr), len(arr[0])
	out = [i[:] for i in arr]
	#print(l,w)
	for i in range(l):
		for j in range(w):
			neighbor_count = sum([arr[x][y] for x,y in neighbors(i,j) if 0<=x<l and 0<=y<w])
			if not(arr[i][j]) and neighbor_count==3: out[i][j] = not(out[i][j])
			if arr[i][j] and (neighbor_count < 2 or neighbor_count > 3): out[i][j] = not(out[i][j])
	return out


L = W = 1000
arr = [[False for j in range(W)] for i in range(L)]
"""
arr[1][1] = True
arr[2][3] = True
arr[3][1] = True
arr[3][2] = True
arr[3][3] = True
"""

r_pentomino = [(500+x,500+y) for x,y in [(0,1),(0,2),(1,0),(1,1),(2,1)]]
for x,y in r_pentomino:
	arr[x][y] = True

def print_arr(arr):
	for row in arr:
		print("".join(['#' if i else ' ' for i in row]))

for i in range(200):
	print(i)
#	print_arr(arr)
	arr = next_gen(arr)
