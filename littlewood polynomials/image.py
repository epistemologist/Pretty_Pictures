import numpy as np
import imageio
import time
IMAGE_SIZE = 500
pixels = np.zeros((IMAGE_SIZE,IMAGE_SIZE))
start = time.time()
def generate_root_histogram(n):
    roots = []
    max_norm = 0
    for i in range(2**(n-1)):
        if i%1000 == 0 and i > 0: 
            elapsed_time = time.time()-start
            eta = elapsed_time / i * (2**(n-1))
            print(i, elapsed_time, eta)
        temp = [int(j) for j in (bin(i)[2:])]
        temp = [0 for i in range(n-1-len(temp))]+temp
        temp = [2*i-1 for i in temp]
        roots = np.roots(temp)
        for j in roots:
            j = j*IMAGE_SIZE/2
            #print(j)
            pixels[int(abs(j.real)),int(abs(j.imag))] += 1
            if j.real**2 + j.imag**2 > max_norm: max_norm = j.real**2 + j.imag**2
    return max_norm
max_norm = generate_root_histogram(25)
pixels = pixels * (255/np.amax(pixels))
print(np.amax(pixels))
pixels = pixels.astype("uint8")
print(pixels)
"""
histogram = [0 for i in range(300)]
for i in pixels.flatten():
    histogram[i] += 1
print(histogram)
"""
imageio.imwrite("out.png",pixels)
