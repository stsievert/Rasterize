#!/usr/bin/python
from __future__ import division
from PIL import Image
import numpy as np
import pudb as pdb
from numpy import *
import matplotlib.pyplot as plt
import argparse

def main():
    # parse the commands, etc. stolen from Matt's code
    PARSER = argparse.ArgumentParser(description='Convert an image to a new ' + 
                                                 'size and color fidelity.')
    PARSER.add_argument('image', help='The image to be converted.')
    PARSER.add_argument('-c', '--colors', type=int,
                        help='Number of colors to use in converting the ' + 
                             ' image.')
    PARSER.add_argument('-w', '--width', type=int,
                        help='Width of the output image, in pixels. Default 300')
    PARSER.add_argument('-t', '--height', type=int,
                        help='Height of the output image, in pixels. Default 300')

    ARGS = PARSER.parse_args()
    FILE = ARGS.image

    if ARGS.width != None:
        width = ARGS.width
    else:
        width = 300
    if ARGS.height != None:
        height = ARGS.height
    else:
        height = 300
    if ARGS.colors != None:
        COLORS = ARGS.colors
    else:
        COLORS = 15

    im = Image.open(FILE)
    im = im.resize((width, height), Image.ANTIALIAS)

    # the above two elements are arguments you can change if you want.

    pix = np.array(Image.open(FILE))
    bw = np.mean(pix, axis=2)
    # bw is now the image in black and white
    #print " after converting from image...\n", np.round(bw)

    bw = rasterize(bw, COLORS)
    #print "after rasterizing...\n", np.round(bw)
    bw = 255 - bw

    bw = make_into_circles(bw, COLORS)

    im = Image.fromarray(bw)
    return im.show()

def make_into_circles(bw, COLORS):
    # each pixel's "color" = radius
    # we use 100*shape to get an approximation of a ball
    N = int(np.round(2 * bw.max() / 16))
    #print N
    w, l = bw.shape
    i = np.arange(0, w)
    j = np.arange(0, l)
    new = np.zeros((N*w, N*l))

    for x in i:
        for y in j:
           #for k in range(0, COLORS):
               #radius = 0
               #if (bw[y,x]>255*k/COLORS) & (bw[y,x]<=255*(k+1)/COLORS):
               #    radius = k+1
            radius = bw[y,x] / 16

            new[N*y:N*y+N, N*x:N*x+N] = makecircle2(new[N*y:N*y+N,
                N*x:N*x+N], radius)
    return new

def rasterize(array, sizes):
    #print array.max()
    #pdb.set_trace()

    for y in range(0,array.shape[0]-1):
        for x in range(0, array.shape[1]-1):
            MAX = array.max()
            oldpix = array[y, x]
            newpix = find_closest_palette_color(oldpix, sizes, MAX)
            quant_error = oldpix - newpix
            try:
                array[y, x] = newpix
                array[y,   x+1] = array[y,   x+1] + 7/16 * quant_error
                array[y+1, x-1] = array[y+1, x-1] + 3/16 * quant_error
                array[y+1,   x] = array[y+1,   x] + 5/16 * quant_error
                array[y+1, x+1] = array[y+1, x+1] + 1/16 * quant_error
            except:
                array = array
    return array

def find_closest_palette_color(value, COLORS, MAX):
    """ does a operation where it goes from 255 colors to desired colors
        returns a value between 0 and 15. needs to return 255/k or something"""
    # choose a value at nearest step size
    # ie, 4 colors: 0-63, 64-128, 128-192, 192-255

    value = value / MAX
    # make the value between 0 and 1

    value = value * (COLORS-1)
    # and make it between 0 and COLORS

    # rounding put values to 0, 1, 2 if 2 colors
    # we want 0, 1. hence the COLORS-1

    value = np.around(value)
    # then round it

    value = value * 255 / COLORS
    # then scale the value between 0 and 255 again

    # and return a rounded int
    return int(np.round(value))

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

if __name__ == '__main__':
    main()



