from PIL import Image
from collections import Counter
filename = "out.png"
im = Image.open(filename)
pixels = []
for pixel in im.getdata():
    pixels.append(pixel)
colors = Counter(pixels)
print(colors)
