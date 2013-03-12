from __future__ import division
from PIL import Image
import numpy as np
import pudb as pdb
from numpy import *
import matplotlib.pyplot as plt

def main():
    COLORS = 12
    FILE = 'len_std.jpg'
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
    im.show()
    return bw

def make_into_circles(bw, COLORS):
    # each pixel's "color" = radius
    # we use 100*shape to get an approximation of a ball
    N = int(np.round(2 * bw.max() / 16))
    print N
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
    print array.max()
    pdb.set_trace()

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




def matplotlib_rast_demo():
    """ from http://matplotlib.org/examples/misc/rasterization_demo.html"""

    d = np.arange(100).reshape(10, 10)
    x, y = np.meshgrid(np.arange(11), np.arange(11))

    theta = 0.25*np.pi
    xx = x*np.cos(theta) - y*np.sin(theta)
    yy = x*np.sin(theta) + y*np.cos(theta)

    ax1 = plt.subplot(221)
    ax1.set_aspect(1)
    ax1.pcolormesh(xx, yy, d)
    ax1.set_title("No Rasterization")

    ax2 = plt.subplot(222)
    ax2.set_aspect(1)
    ax2.set_title("Rasterization")

    m = ax2.pcolormesh(xx, yy, d)
    m.set_rasterized(True)

    ax3 = plt.subplot(223)
    ax3.set_aspect(1)
    ax3.pcolormesh(xx, yy, d)
    ax3.text(0.5, 0.5, "Text", alpha=0.2,
             va="center", ha="center", size=50, transform=ax3.transAxes)

    ax3.set_title("No Rasterization")


    ax4 = plt.subplot(224)
    ax4.set_aspect(1)
    m = ax4.pcolormesh(xx, yy, d)
    m.set_zorder(-20)

    ax4.text(0.5, 0.5, "Text", alpha=0.2,
             zorder=-15,
             va="center", ha="center", size=50, transform=ax4.transAxes)

    ax4.set_rasterization_zorder(-10)

    ax4.set_title("Rasterization z$<-10$")


    # ax2.title.set_rasterized(True) # should display a warning

    plt.savefig("test_rasterization.pdf", dpi=150)
    plt.savefig("test_rasterization.eps", dpi=150)

    if not plt.rcParams["text.usetex"]:
        plt.savefig("test_rasterization.svg", dpi=150)
        # svg backend currently ignores the dpi
















