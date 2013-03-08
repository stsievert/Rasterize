from __future__ import division
from PIL import Image
import numpy as np
import pudb as pdb
from numpy import *
def main():
    COLORS = 15
    FILE = 'len_std.jpg'
    # the above two elements are arguments you can change if you want.

    N = 1.8*COLORS
    pix = np.array(Image.open(FILE))
    bw = np.mean(pix, axis=2)
    # bw is now the image in black and white

    w, l = bw.shape
    new = np.zeros((N*w, N*l))

    # each pixel's "color" = radius
    # we use 100*shape to get an approximation of a ball
    i = np.arange(0, w)
    j = np.arange(0, l)


    for x in i:
        for y in j:
            for k in range(0, COLORS):
                if (bw[y,x]>255*k/COLORS) & (bw[y,x]<=255*(k+1)/COLORS):
                    radius = k+1

            new[N*y:N*y+N, N*x:N*x+N] = makecircle2(new[N*y:N*y+N,
                N*x:N*x+N], radius)
    im = Image.fromarray(new)
    im.show()


def rasterize(pixel):
    print pixel.shape[0]
    print pixel.shape[1]
    pdb.set_trace()
    for y in range(0,pixel.shape[0]-1):
        for x in range(0, pixel.shape[1]-1):
            oldpixel = pixel[y, x]
            newpixel = find_closest_palette_color(oldpixel)
            quant_error = oldpixel - newpixel
            print quant_error
            pixel[y, x] = newpixel
            pixel[y,   x+1] = pixel[y,   x+1] + 7/16 * quant_error
            pixel[y+1, x-1] = pixel[y+1, x-1] + 3/16 * quant_error
            pixel[y+1,   x] = pixel[y+1,   x] + 5/16 * quant_error
            pixel[y+1, x+1] = pixel[y+1, x+1] + 1/16 * quant_error
    return pixel

def makecircle2(pixels, radius):
    """ assumes pixels is a 100x100 array. makes a circle of radius """
    x = np.arange(-pixels.shape[0]//2, pixels.shape[0]//2)
    y = np.arange(-pixels.shape[1]//2, pixels.shape[1]//2)
    x, y = np.meshgrid(x, y)
    circle = np.zeros((len(y), len(x)))
    i = radius < np.sqrt(np.power(x, 2) + np.power(y, 2))
    try: circle[i] = 255
    except: f = 0
    
    return circle






















