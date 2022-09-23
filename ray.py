from lib import *
from math import *
from sphere import *

class Raytracer (object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear_color = color(0,0,0)
        self.current_color = color(255,255,255)
        self.clear()
        
    def clear(self):
        self.framebuffer = [
        [self.clear_color for x in range (self.width)]
        for y in range(self.height)
        ]
    
    def point(self,x,y,c=None):
        if y >= 0 and y < self.height and x>=0 and x<self.width:
            self.framebuffer[y][x] = c or self.current_color
            
    def write(self, filename):
        writebmp(filename,self.width,self.height, self.framebuffer )
    
    def cast_ray(self,origin,direction):
        s = Sphere(V3(-3,0,-16),2)
        if s.ray_intersect(origin,direction):
            return color(255,0,0)
        else:
            return self.clear_color
    
    def render(self):
        fov = int(pi/2)
        ar = self.width/self.height
        tana = tan(fov/2)
        
        for y in range(self.height):
            for x in range(self.width):
                i=((2* (x*0.5) / self.width ) -1) *ar*tana
                j=((2* (y*0.5) / self.height ) -1) *ar*tana
                
                direction = norm(V3(i,j,-1))
                origin = V3(0,0,0)
                c = self.cast_ray(origin,direction)
                self.point(y,x,c)
                
    
        
r = Raytracer(400,400)
r.point(100,100)
r.render()
r.write('r.bmp')