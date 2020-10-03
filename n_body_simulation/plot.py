from PIL import Image
def plot_points(points, w, h, filename):
    # assuming points is array of [x,y,r,g,b]
    # x,y being position
    # r,g,b being color of particle
    im = Image.new("RGB",(w,h),"white")
    x_values = [i[0] for i in points]
    y_values = [i[1] for i in points]
    x_min = min(x_values)
    x_max = max(x_values)
    y_min = min(y_values)
    y_max = max(y_values)
    for i in points:
        x,y,r,g,b = i[0],i[1],i[2],i[3],i[4]
        new_x = int((w-1)*(x-x_min)/(x_max-x_min))
        new_y = int((h-1)*(y-y_min)/(y_max-y_min))
        print(new_x,new_y)
        im.putpixel((new_x,new_y),(r,g,b))
    im.save(filename)
plot_points([[1,1,0,255,255],[2,2,0,0,255],[3,3,255,0,255]],50,50,"out.png")
