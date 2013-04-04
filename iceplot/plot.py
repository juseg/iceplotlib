"""iceplot.plot

Provide the actual plotting interface
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm, Normalize

from iceplot import cm as icm
from iceplot import figure as ifig

### Figure functions ###

def gridfigure(mapsize, nrows_ncols, **kwargs):
		"""Create a new figure and return a pismplot.figure.GridFigure instance"""
		return plt.figure(FigureClass=ifig.GridFigure,
      mapsize=mapsize, nrows_ncols=nrows_ncols, **kwargs)

def simplefigure(mapsize, **kwargs):
		"""Create a new figure and return a pismplot.figure.SimpleFigure instance"""
		return plt.figure(FigureClass=ifig.SimpleFigure,
      mapsize=mapsize, **kwargs)

def doubleinlinefigure(mapsize, **kwargs):
		"""Create a new figure and return a pismplot.figure.DoubleInlineFigure instance"""
		return plt.figure(FigureClass=ifig.DoubleInlineFigure,
      mapsize=mapsize, **kwargs)

### Plotting functions ###

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
      cmap=icm.topo,
      norm=Normalize(-6000,6000))

    # draw surface velocity
    im = plt.imshow(csurf,
      cmap = icm.velocity,
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

def bedtempmap(nc, t=0):
    """Draw basal pressure-adjusted temperature map"""

    # extract variables
    temp  = nc.variables['temppabase'][t].T
    thk   = nc.variables['thk'][t].T
    temp  = np.ma.masked_where(thk < 1, temp)

    # draw basal temperature contours
    levs = [-10, -8, -6, -4, -2, -1e-3, 0]
    cs = plt.contourf(temp,
      levels = levs,
      cmap   = plt.cm.Blues_r,
      extend = 'min')
    plt.contour(temp,
      levels = levs,
      colors = 'white',
      linewidths = 0.2,
      linestyles = 'solid')

    # draw ice outline
    plt.contour(thk,
      levels     = [1, 5000],
      colors     = 'black',
      linewidths = 1)

    # return contour set for colormaps
    return cs

def bedvelmap(nc, t=0):
    """Draw basal velocity map"""

    # extract variables
    x    = nc.variables['x'][:]
    y    = nc.variables['y'][:]
    uvel = nc.variables['uvelbase'][t].T
    vvel = nc.variables['vvelbase'][t].T
    thk  = nc.variables['thk'][t].T

    # draw streamplot
    ss = plt.streamplot(x, y, uvel, vvel,
      density=5,
      color='black',
      linewidth=0.2)

    # draw ice outline
    plt.contour(thk,
      levels     = [1, 5000],
      colors     = 'black',
      linewidths = 1)

    # return stream plot set
    return ss

