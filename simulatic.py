#!/usr/bin/python

'''Converts an image to a fixed color palette and optionally a fixed size.'''

# credit goes to http://stackoverflow.com/a/237193/254187
#            and http://stackoverflow.com/a/237747/254187

import Image
import argparse
import os

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

PARSER = argparse.ArgumentParser(description='Convert an image to a new ' + 
                                             'size and color fidelity.')
PARSER.add_argument('image', help='The image to be converted.')
PARSER.add_argument('-c', '--colors', type=int,
                    help='Number of colors to use in converting the ' + 
                         ' image. Maximum (default) is ' + str(len(COLORS)) + 
                         '.')
PARSER.add_argument('-w', '--width', type=int,
                    help='Width of the output image, in pixels.')
PARSER.add_argument('-t', '--height', type=int,
                    help='Height of the output image, in pixels.')

ARGS = PARSER.parse_args()

IMGPATH = ARGS.image

if ARGS.colors != None:
    NUMCOLORS = ARGS.colors
else:
    NUMCOLORS = len(COLORS)

DO_RESIZE = False
if ARGS.height != None and ARGS.width != None:
    DO_RESIZE = True
    HEIGHT = ARGS.height
    WIDTH = ARGS.width
    NEW_SIZE = (WIDTH, HEIGHT)

# add the first NUMCOLORS colors from COLORS to PALETTE
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

# resize it to our target size
if DO_RESIZE:
    print 'Resizing image to ' + str(WIDTH) + 'x' + str(HEIGHT)
    imagec = imagec.resize(NEW_SIZE, Image.ANTIALIAS)

# quantize it using our palette image
imagep = imagec.quantize(palette=pimage)

# save
imagep.save(newpathname)
