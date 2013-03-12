The code that goes with our paint-a-new-picture-everyday on the side of Amundson
project. This code is stored as an iPython notebook. It is viewable [here][1].

It is recommended that you install NumPy, Matplotlib and PIL so you can actually
edit the files. To do that, look at this [Python installation guide.][2]
Enthought is free for academia users, and the SciPy SuperPack also works. You
can also run `sudo pip install numpy PIL matplotlib pudb`.

If you're actually using the Python script, it returns an array, but shows the
image in the meantime (using your default image viewer).

The program follows the same layout as Matt's simulatic program. The usage is
`python rasterize.py IMAGE -w WIDTH -t HEIGHT -c NUMBER OF SIZES`. Note that it
only works for perfectly square images right now, but the width and height can
not be square.

[1]:http://nbviewer.ipython.org/5143813
[2]:http://scipy.github.com/download.html
