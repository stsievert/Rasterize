#from __future__ import division
from PIL import Image
import numpy as np
from numpy import *

def main():
    file = r'len_std.jpg'
    pix = np.array(Image.open(file))
    bw = np.mean(pix, axis=2)
    # bw is now the image in black and white
    
    new = np.zeros((100*bw.shape[0], 100*bw.shape[1]))

    # each pixel's "color" = radius
    # we use 100*shape to get an approximation of a ball
    i = np.arange(0, bw.shape[0])
    j = np.arange(0, bw.shape[0])

    for x in i[0:-1]:
        for y in j[0:-1]:
            new[100*y:100*y+100, 100*x:100*x+100] = makecircle2(new[100*y:100*y+100,
                100*x:100*x+100], bw[y,x])
    return new


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
    circle[i] = 255
    return circle






















