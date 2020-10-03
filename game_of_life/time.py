import time

# Construct N
n = [1,4]
for i in range(16):
	n.append(n[-1]**2)
N = reduce(lambda x,y:x*y, [i+1 for i in n])


def time_f(f):
	start = time.time()
	f()
	end = time.time()
	return end-start

def bit_int(N=N):
	nth_bits = lambda N, k, p: ((1<<k)-1) & (N >> p)
	for i in range(30):
		out = nth_bits(N,3,i)

def bit_arr(arr=list(map(int,list(bin(N)[2:])))):
	for i in range(30):
		out = arr[i:i+3]


print(time_f(bit_int))
print(time_f(bit_arr))
