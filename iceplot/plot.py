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

### Data extraction ###

def _extract(nc, varname, t):
    var = nc.variables[varname]
    """Extract data from a netcdf file"""

    if t == 'djf':
      return var[[12,0,1]].mean(axis=2).T
    if t == 'mam':
      return var[2:5].mean(axis=2).T
    if t == 'jja':
      return var[6:8].mean(axis=2).T
    if t == 'son':
      return var[9:11].mean(axis=2).T
    if t == 'mean':
      return var[:].mean(axis=2).T
    else:
      return var[t].T

### Image mapping functions ###

def bedtopoimage(nc, t=0, **kwargs):
    """Draw bed topography."""
    topg  = _extract(nc, 'topg', t)
    return mplt.imshow(topg,
      cmap = kwargs.pop('cmap', icm.topo),
      norm = kwargs.pop('norm', mcolors.Normalize(-6000,6000)),
      **kwargs)

def airtempimage(nc, t=0, **kwargs):
    """Draw near-surface air temperature."""
    temp = _extract(nc, 'air_temp', t)
    return mplt.imshow(temp,
      cmap = kwargs.pop('cmap', mplt.cm.Spectral_r),
      norm = kwargs.pop('norm', mcolors.Normalize(-30,30)),
      **kwargs)

def precipimage(nc, t=0, **kwargs):
    """Draw precipitation rate."""
    prec = _extract(nc, 'precipitation', t)
    return mplt.imshow(prec,
      cmap = kwargs.pop('cmap', mplt.cm.YlGnBu),
      norm = kwargs.pop('norm', mcolors.LogNorm(0.1,10)),
      **kwargs)

def surfvelimage(nc, t=0, **kwargs):
    """Draw surface velocity."""
    thk   = _extract(nc, 'thk', t)
    csurf = _extract(nc, 'csurf', t)
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
    thk = _extract(nc, 'thk', t)
    return mplt.contour(thk,
      levels     = [kwargs.pop('level', 1)],
      colors     = [kwargs.pop('color', 'black')],
      **kwargs)

def surftopocontour(nc, t=0, **kwargs):
    """Draw ice surface topography contours."""
    thk   = _extract(nc, 'thk', t)
    usurf = _extract(nc, 'usurf', t)
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
    temp  = _extract(nc, 'temppabase', t)
    thk   = _extract(nc, 'thk', t)
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
    uvel = _extract(nc, 'uvelbase', t)
    vvel = _extract(nc, 'vvelbase', t)
    cbase= _extract(nc, 'cbase', t)
    temp = _extract(nc, 'temppabase', t)
    thk  = _extract(nc, 'thk', t)
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

