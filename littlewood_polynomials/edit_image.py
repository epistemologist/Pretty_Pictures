from PIL import Image
im = Image.open("out.png")
im2 = Image.new("RGB", (2000,2000), "black")
for i in range(2000):
    for j in range(2000):
        temp = im.getpixel((i,j))
        if temp != 0:
            im2.putpixel((i,j),(255,255,255))
im2.save("out2.png")
