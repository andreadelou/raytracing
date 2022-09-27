import struct

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b*255),
                    int(g*255),
                    int(r*255)])
    

def clamping(num):
    return int(max(min(num, 255), 0))


BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


def Clear(self):
  self.framebuffer = [
    [color(0,0,0) for x in range(self.width)] 
    for y in range(self.height)
  ]


def ClearColor(self, r, g, b):
    self.clearColor = color(r, b, g)
    self.Clear()


def writebmp(filename, width, height, framebuffer):
    f = open(filename, 'bw')

    # pixel header
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + width * height * 3))
    f.write(word(0))
    f.write(word(0))
    f.write(dword(14 + 40))

    # info header
    f.write(dword(40))
    f.write(dword(width))
    f.write(dword(height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(width * height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # pixel data
    for x in range(height):
        for y in range(width):
            f.write(framebuffer[y][x])

    f.close()


def set_current_color(self, r, g, b):
    red = self.clamping(r * 255)
    green = self.clamping(g * 255)
    blue = self.clamping(b * 255)
    self.current_color = color(red, green, blue)


def point(self, x, y):
    if x >= 0 and x < self.width and y >= 0 and y < self.height:
        self.framebuffer[x][y] = self.current_color


def line(self, v1, v2):

    x0 = round(v1.x)
    x1 = round(v2.x)
    y0 = round(v1.y)
    y1 = round(v2.y)

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    steep = dy > dx

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    offset = 0
    threshold = dx
    y = y0

    for x in range(x0, x1 + 1):
        if steep:
            self.point(y, x)
        else:
            self.point(x, y)

        offset += dy * 2

        if offset >= threshold:
            y += 1 if y0 < y1 else -1

            threshold += dx * 2