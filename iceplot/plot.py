# coding: utf-8
"""iceplot.plot

Provide the actual plotting interface
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm, Normalize

def icemap(nc, t=0):
    """Draw basal topography, surface velocity and elevation contours"""

    # extract variables
    topg  = nc.variables['topg'][t].T
    thk   = nc.variables['thk'][t].T
    csurf = nc.variables['csurf'][t].T
    usurf = nc.variables['usurf'][t].T
    usurf = np.ma.masked_where(thk < 1, usurf)

    # draw bed topography
    plt.imshow(topg,
      cmap=plt.cm.terrain,
      norm=Normalize(-3000,6000))

    # draw surface velocity
    im = plt.imshow(csurf,
      cmap = plt.cm.Greys,
      norm = LogNorm(10, 10000))

    # draw ice outline
    plt.contour(thk,
      levels     = [1, 5000],
      colors     = 'black',
      linewidths = 1)

    # draw ice topography contours
    plt.contour(usurf,
      levels     = range(1000, 5000, 1000),
      colors     = 'black',
      linewidths = 0.5)

    # return velocity image for colormaps
    return im

