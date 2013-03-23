#!/usr/bin/python
from __future__ import division
from PIL import Image
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import argparse
import os
from pylab import *
FILE = 'len_std.jpg'

def make_into_circles(bw, COLORS):
    # each pixel's "color" = radius
    # we use 100*shape to get an approximation of a ball
    N = int(np.round(2 * bw.max() / 16))
    #print N
    N = 16
    c, w, l = bw.shape # c == 3
    i = np.arange(0, w)
    j = np.arange(0, l)
    new = np.zeros((3, N*w, N*l))

    for x in i:
        for y in j:
            radius = 4
            color = bw[:,y,x]

            new[:,N*y:N*y+N, N*x:N*x+N] = makecircle2(
                new[N*y:N*y+N, N*x:N*x+N], radius, color)
    return new
def simulatic(array, sizes):
    """ assumes a 3 dimensional array for colors. this code is simply transforms
    the image into so many colors """
    # contains the target rasterized color values for the image
    PALETTE = []

    # contains the colors to push onto the palette
    COLORS = [
        [0,   0,   0  ], # black
        [255, 255, 255], # white

        [255, 0,   0  ], # red
        [0,   255, 0  ], # green
        [0,   0,   255], # blue

        [0,   255, 255], # cyan
        [255, 0,   255], # magenta
        [255, 255, 0  ]  # yellow
    ]
    IMGPATH = FILE
        

    # add the first NUMCOLORS colors from COLORS to PALETTE
    NUMCOLORS = 4
    for colornum in range(NUMCOLORS):
        try:
            PALETTE += COLORS.pop(0)
        except IndexError:
            print('WARNING: ' + str(NUMCOLORS) + ' colors requested but only ' + 
                  str(colornum) + ' colors available, using the first ' + 
                  str(colornum) + ' colors')
            NUMCOLORS = str(colornum)
            break
    
    # pad PALETTE to 768 values (256 * RGB (3) = 768)
    if len(PALETTE) < 768:
        PALETTE += [0] * (768 - len(PALETTE))

    dirname, filename = os.path.split(IMGPATH)
    name, ext = os.path.splitext(filename)
    newpathname = os.path.join(dirname, "conv-%s.png" % name)
    print('Processing ' + IMGPATH + ' to ' + str(NUMCOLORS) + ' colors as ' +
          newpathname)

    # a palette image to use for quant
    pimage = Image.new("P", (1, 1), 0)
    pimage.putpalette(PALETTE)

    # open the source image
    imagef = Image.open(IMGPATH)
    imagec = imagef.convert("RGB")

    # quantize it using our palette image
    imagep = imagec.quantize(palette=pimage)

    return imagep
def find_closest_palette_color(value, COLORS, MAX):
    """ finds the closest color: stolen from matt's simulatic"""
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
def makecircle2(pixels, radius, color):
    """ assumes pixels is a 100x100 array. makes a circle of radius """
    x = np.arange(-pixels.shape[0]//2, pixels.shape[0]//2)
    y = np.arange(-pixels.shape[1]//2, pixels.shape[1]//2)
    x, y = np.meshgrid(x, y)
    circle = np.zeros(( 3, len(y), len(x)))
    i = radius < np.sqrt(np.power(x, 2) + np.power(y, 2))
    try: 
        circle[0, i] = color[0]
        circle[1, i] = color[1]
        circle[2, i] = color[2]
    except: f = 0
    
    return circle

def parse_args():
    """parse the commands, etc. stolen from Matt's code"""
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

    return FILE, width, height, COLORS

def makeColoredCircle(arr, color):
    """ makes a colored circle...
        assumes arr is the actual size (100x100, not 1x1)
        assumes that arr is 3 colors, not 1 dimension"""

    radius = arr.shape[0]/2
    xx = arange(-arr.shape[0]//2, arr.shape[1]//2)
    yy = arange(-arr.shape[0]//2, arr.shape[1]//2)
    x, y = meshgrid(xx, yy)
    i = radius > sqrt(x**2 + y**2)
    arr[i] = color
    return arr
colors = [
    [0,   0,   0  ], # black
    [255, 255, 255], # white

    [255, 0,   0  ], # red
    [0,   255, 0  ], # green
    [0,   0,   255], # blue

    [0,   255, 255], # cyan
    [255, 0,   255], # magenta
    [255, 255, 0  ]  # yellow
]

#FILE, width, height, COLORS = parse_args()

# change as you need to
FILE = 'lenna-300x300.png'
#width, height = (300, 300)
COLORS = 4



# arr is the original image...
#FILE = 'lenna-300x300.png'
mul = 24
ar = imread(FILE)

# it's the original image in 4 colors now (as an image)
sim = simulatic(ar, 4)

# and now as an array
arr = array(sim)
print arr.shape

# imshow() takes values between 0 and 1

w, l = arr.shape
new = ones((mul*w, mul*l, 3))
for i in range(w):
    for j in range(l):
        new[mul*i:mul*i+mul, mul*j:mul*j+mul] = makeColoredCircle(
            new[mul*i:mul*i+mul, mul*j:mul*j+mul], 
            array(colors[arr[i,j]])/255)

outfile = FILE.partition('.')[0]
ax = figure()
imshow(new)
axis('off')
savefig('conv-'+outfile+'.pdf',dpi=500, bbox_inches='tight')














