# plotting utilities
from PIL import Image, ImageDraw
from math import sqrt
from matplotlib import cm
import random
def plot_points(points, w, h, filename, x_range=None, y_range=None):
    # assuming points is array of [x,y,r,g,b]
    # x,y being position
    # r,g,b being color of particle
    im = Image.new("RGB",(w,h),"white")
    x_values = [i[0] for i in points]
    y_values = [i[1] for i in points]
    if x_range == None or y_range == None:
        x_min = min(x_values)
        x_max = max(x_values)
        y_min = min(y_values)
        y_max = max(y_values)
    else:
        x_min = x_range[0]
        x_max = x_range[1]
        y_min = y_range[0]
        y_max = y_range[1]    
    for i in points:
        x,y,r,g,b = i[0],i[1],i[2],i[3],i[4]
        new_x = int((w-1)*(x-x_min)/(x_max-x_min))
        new_y = int((h-1)*(y-y_min)/(y_max-y_min))
        if 0<=new_x<w and 0<=new_y<h:
            im.putpixel((new_x,new_y),(r,g,b))
    im.save(filename)
def plot_points_circles(points, w, h, filename, x_range=None, y_range=None, r=3):
    # assuming points is array of [x,y,r,g,b]
    # x,y being position
    # r,g,b being color of particle
    im = Image.new("RGB",(w,h),"black")
    draw = ImageDraw.Draw(im)
    x_values = [i[0] for i in points]
    y_values = [i[1] for i in points]
    if x_range == None or y_range == None:
        x_min = min(x_values)
        x_max = max(x_values)
        y_min = min(y_values)
        y_max = max(y_values)
    else:
        x_min = x_range[0]
        x_max = x_range[1]
        y_min = y_range[0]
        y_max = y_range[1]
    for i in points:
        x,y,red,green,blue = i[0],i[1],i[2],i[3],i[4]
        new_x = int((w-1)*(x-x_min)/(x_max-x_min))
        new_y = int((h-1)*(y-y_min)/(y_max-y_min))
        if 0<=new_x<w and 0<=new_y<h:
            draw.ellipse([new_x-r,new_y-r,new_x+r,new_y+r],fill=(red,green,blue))
    im.save(filename)
def plot_particles(particles,w,h,filename,x_range=None,y_range=None):
    points = [[p.px,p.py,p.color[0],p.color[1],p.color[2]] for p in particles]
    plot_points(points,w,h,filename,x_range=x_range,y_range=y_range)
def plot_particles_circles(particles,w,h,filename,r,x_range=None,y_range=None):
    points = [[p.px,p.py,p.color[0],p.color[1],p.color[2]] for p in particles]
    plot_points_circles(points,w,h,filename,x_range=x_range,y_range=y_range,r=r)
# Particle class
class Particle:
    def __init__(self,px,py,vx,vy,mass=1,color=(255,255,255)):
        self.mass = mass
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.color = color
dt = 0.005
particles = [Particle(0,0,0,0,mass=1000)]
for i in range(0,250,10):
    particles.append(Particle(5,0,0,i*0.2,color=[int(255*j) for j in cm.hsv(i)[:3]]))
def next(filename):
    accelerations = [None for i in particles]
    # get the accelerations of particles
    for i in range(len(particles)):
        particle_i = particles[i]
        current_force_x = 0
        current_force_y = 0
        qix = particle_i.px
        qiy = particle_i.py
        mi = particle_i.mass
        for j in range(len(particles)):
            if j==0 and i!=0:
                particle_j = particles[j]
                qjx = particle_j.px
                qjy = particle_j.py
                mj = particle_j.mass
                temp = (mi*mj) * (sqrt((qjx-qix)**2+(qjy-qiy)**2))**-1.5
                current_force_x += temp * (qjx-qix)
                current_force_y += temp * (qjy-qiy)
        accelerations[i] = (current_force_x/mi,current_force_y/mi)
    # update positions and velocities of particles
    for i in range(len(particles)):
        p = particles[i]
        px,py,vx,vy = p.px,p.py,p.vx,p.vy
        ax,ay = accelerations[i]
        new_px = px+vx*dt+0.5*ax*dt**2
        new_py = py+vy*dt+0.5*ay*dt**2
        new_vx = vx+ax*dt
        new_vy = vy+ay*dt
        p.px = new_px
        p.py = new_py
        p.vx = new_vx
        p.vy = new_vy
    # color particles based on density
    """
    colors = []
    for i in range(len(particles)):
        distances = []
        ix = particles[i].px
        iy = particles[i].py
        for j in range(len(particles)):
            jx = particles[j].px
            jy = particles[j].py
            distances.append(sqrt((ix-jx)**2+(iy-jy)**2))
        colors.append(sum(distances)/len(distances))
    min_colors,max_colors = min(colors),max(colors)
    colors = [[int(255*j) for j in cm.hot_r(int((i-min_colors)*255/(max_colors-min_colors)))] for i in colors]
    for i in range(len(particles)):
        particles[i].color = colors[i][:3]
    """
    plot_particles_circles(particles,1000,1000,filename,x_range=(-20,20),y_range=(-20,20),r=3)
for i in range(10000):
    print(i)
    next(str(i)+".png")
