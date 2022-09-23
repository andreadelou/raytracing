from pickletools import read_unicodestring1


class Sphere(object):
    def __init__(self, center, radius) :
        self.center = center
        self.radius = radius
        
    def ray_intersect(self,origin,direction):
        return True