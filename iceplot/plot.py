"""iceplot.plot

Provide the actual plotting interface
"""

import numpy as np
from matplotlib import pyplot as mplt
from matplotlib import colors as mcolors

from iceplot import cm as icm
from iceplot import figure as ifig

### Figure functions ###

def gridfigure(mapsize, nrows_ncols, **kwargs):
		"""Create a new figure and return a pismplot.figure.GridFigure instance"""
		return mplt.figure(FigureClass=ifig.GridFigure,
      mapsize=mapsize, nrows_ncols=nrows_ncols, **kwargs)

def simplefigure(mapsize, **kwargs):
		"""Create a new figure and return a pismplot.figure.SimpleFigure instance"""
		return mplt.figure(FigureClass=ifig.SimpleFigure,
      mapsize=mapsize, **kwargs)

def doubleinlinefigure(mapsize, **kwargs):
		"""Create a new figure and return a pismplot.figure.DoubleInlineFigure instance"""
		return mplt.figure(FigureClass=ifig.DoubleInlineFigure,
      mapsize=mapsize, **kwargs)

### Image mapping functions ###

def bedtopoimage(nc, t=0, **kwargs):
    """Draw bed topography."""
    topg  = nc.variables['topg'][t].T
    return mplt.imshow(topg,
      cmap = kwargs.pop('cmap', icm.topo),
      norm = kwargs.pop('norm', mcolors.Normalize(-6000,6000)),
      **kwargs)

def airtempimage(nc, t=0, **kwargs):
    """Draw near-surface air temperature."""
    temp = nc.variables['air_temp'][t].T
    return mplt.imshow(temp,
      cmap = kwargs.pop('cmap', mplt.cm.Spectral_r),
      norm = kwargs.pop('norm', mcolors.Normalize(-30,30)),
      **kwargs)

def precipimage(nc, t=0, **kwargs):
    """Draw precipitation rate."""
    prec = nc.variables['precipitation'][t].T
    return mplt.imshow(prec,
      cmap = kwargs.pop('cmap', mplt.cm.YlGnBu),
      norm = kwargs.pop('norm', mcolors.LogNorm(0.1,10)),
      **kwargs)

def surfvelimage(nc, t=0, **kwargs):
    """Draw surface velocity."""
    thk   = nc.variables['thk'][t].T
    csurf = nc.variables['csurf'][t].T
    csurf = np.ma.masked_where(thk < 1, csurf)
    return mplt.imshow(csurf,
      cmap = kwargs.pop('cmap', icm.velocity),
      norm = kwargs.pop('norm', mcolors.LogNorm(10, 10000)),
      **kwargs)

### Contour mapping functions ###

## Not used yet
#def _contours(*args, **kwargs):
#    """Wrap :func:`~matplotlib.pyplot.contour` and :func:`~matplotlib.pyplot.contours` in a single function"""
#    if 'fcolors' in kwargs:
#      mplt.contourf(*args, **kwargs)
#    if 'linewidths' in kwargs:
#      mplt.contour(*args, **kwargs)

def icemargincontour(nc, t=0, **kwargs):
    """Draw a contour along the ice margin."""
    thk = nc.variables['thk'][t].T
    return mplt.contour(thk,
      levels     = [kwargs.pop('level', 1)],
      colors     = [kwargs.pop('color', 'black')],
      **kwargs)

def surftopocontour(nc, t=0, **kwargs):
    """Draw ice surface topography contours."""
    thk   = nc.variables['thk'][t].T
    usurf = nc.variables['usurf'][t].T
    usurf = np.ma.masked_where(thk < 1, usurf)
    return mplt.contour(usurf,
      levels     = kwargs.pop('levels', range(1000, 5000, 1000)),
      colors     = kwargs.pop('colors', 'black'),
      linewidths = kwargs.pop('linewidths', 0.5))

### Composite mapping functions ###

def icemap(nc, t=0, **kwargs):
    """Draw basal topography, surface velocity and elevation contours."""

    # draw bed topography
    bedtopoimage(nc, t,
      **{kw: kwargs['bedtopo_'+kw]
        for kw in ('cmap', 'norm') if 'bedtopo_'+kw in kwargs})

    # draw surface velocities
    im = surfvelimage(nc, t,
      **{kw: kwargs['surfvel_'+kw]
        for kw in ('cmap', 'norm') if 'surfvel_'+kw in kwargs})

    # draw surface topography contours
    surftopocontour(nc, t,
      **{kw: kwargs['surftopo_'+kw]
        for kw in ('levels', 'colors') if 'surftopo_'+kw in kwargs})

    # draw ice margin contour
    icemargincontour(nc, t)

    # return surface velocity image
    return im

### TODO: To be developped functions ###

def bedtempmap(nc, t=0):
    """Draw basal pressure-adjusted temperature map"""

    # extract variables
    temp  = nc.variables['temppabase'][t].T
    thk   = nc.variables['thk'][t].T
    temp  = np.ma.masked_where(thk < 1, temp)

    # draw basal temperature contours
    levs = [-10, -8, -6, -4, -2, -1e-3, 0]
    cs = mplt.contourf(temp,
      levels = levs,
      cmap   = mplt.cm.Blues_r,
      extend = 'min')
    mplt.contour(temp,
      levels = levs,
      colors = 'white',
      linewidths = 0.2,
      linestyles = 'solid')

    # draw ice outline
    mplt.contour(thk,
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
    cbase= nc.variables['cbase'][t].T
    temp = nc.variables['temppabase'][t].T
    thk  = nc.variables['thk'][t].T
    temp = np.ma.masked_where(thk < 1, temp)
    cbase= np.ma.masked_where(cbase < 1, cbase)

    uvel = np.sign(uvel)*np.log(1+np.abs(uvel)/100)
    vvel = np.sign(vvel)*np.log(1+np.abs(vvel)/100)

    # draw frozen bed areas
    mplt.contourf(temp,
      colors = '0.75',
      levels = [-1e3, -1e-3])

    # draw streamplot
    ss = mplt.quiver(uvel, vvel, cbase,
      cmap = icm.velocity,
      norm = LogNorm(1, 3000))

    # draw ice outline
    mplt.contour(thk,
      levels     = [1, 5000],
      colors     = 'black',
      linewidths = 1)

    # return stream plot set
    return ss

