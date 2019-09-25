import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from math import sqrt, sin, log10
from matplotlib.colors import ListedColormap
import time
start = time.time()
def f(x): # function that maps [0,1] to itself for the color space so that values closer to 1 end up further from 1
    return x**3
def roots(n): # given n, returns a Littlewood polynomial with coefficients representing the binary representation of n
    return np.polynomial.polynomial.polyroots([int(i)*2-1 for i in bin(n)[2:]])
# get array of all possible roots and split values up into arrays x and y
x, y = [], []
ROOTS = 2**24
for i in range(0,ROOTS):
    if i%10000==0 and i>0:
        elapsed_time = time.time()-start
        eta = elapsed_time / i * ROOTS
        print(i, elapsed_time, eta)
    root = roots(i)
    x.extend(np.abs(np.real(root)))
    y.extend(np.abs(np.imag(root)))

# generate histogram of roots to make heatmap
gap=1.5/2400
print(len(np.arange(0,1.5,gap)))
normal_histogram = np.histogram2d(x,y,bins=np.arange(0,1.5,gap),normed=True)

# generate image 
start = time.time()
from PIL import Image
normal_histogram = normal_histogram[0]
size=len(normal_histogram)
im = Image.new("RGB",(size,size))
im2 = Image.new("RGB",(size,size))
old_prism = cm.get_cmap("hsv",256)
new_colors = old_prism(np.linspace(0,1,256))
black = np.array([0,0,0,0])
new_colors[0] = black
new_prism = ListedColormap(new_colors)
#color = [int(256*k) for k in cm.hot(histogram[i][j])[0:3]]
# plt.plot(normal_histogram.flatten())
# plt.show()
for i in range(len(normal_histogram)):
    elapsed_time = time.time()-start
    eta = elapsed_time / (i+1) * len(normal_histogram)
    print(i, elapsed_time, eta)
    for j in range(len(normal_histogram)):
        temp = int(normal_histogram[i][j]*256)
        im.putpixel((i,j),tuple([int(256*k) for k in new_prism(f(normal_histogram[i][j]))][0:3]))
        im2.putpixel((i,j),tuple([int(256*k) for k in cm.hot(f(normal_histogram[i][j]))][0:3]))
im.save("test.png")
im2.save("test2.png")
