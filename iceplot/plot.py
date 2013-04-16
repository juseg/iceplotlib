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

def _contours(*args, **kwargs):
    """Wrap :func:`~matplotlib.pyplot.contour` and :func:`~matplotlib.pyplot.contours` in a single function."""

    # pop out all special arguments
    colors     = kwargs.pop('colors', None)
    cmap       = kwargs.pop('cmap', None)
    linecolors = kwargs.pop('linecolors', None)
    linecmap   = kwargs.pop('linecmap', None)
    linewidths = kwargs.pop('linewidths', None)
    linestyles = kwargs.pop('linestyles', None)

    # check for filled and lined contours arguments
    has_fill_args = any((colors, cmap))
    has_line_args = any((linecolors, linecmap, linewidths, linestyles))

    # plot filled contours
    cf = None
    if has_fill_args or not has_line_args:
      cf = mplt.contourf(*args,
        cmap   = cmap,
        colors = colors,
        **kwargs)

    # plot lined contours
    cl = None
    if has_line_args or not has_fill_args:
      cl = mplt.contour(*args,
        colors     = linecolors,
        cmap       = linecmap,
        linewidths = linewidths,
        linestyles = linestyles,
        **kwargs)

    # return filled or lined contour set
    return cf or cl

def icemargincontour(nc, t=0, **kwargs):
    """Draw a contour along the ice margin."""
    thk = _extract(nc, 'thk', t)
    return _contours(thk,
      levels     = [kwargs.pop('level', 1), np.inf],
      linecolors = kwargs.pop('linecolors', 'black'),
      **kwargs)

def surftopocontour(nc, t=0, **kwargs):
    """Draw ice surface topography contours."""
    thk   = _extract(nc, 'thk', t)
    usurf = _extract(nc, 'usurf', t)
    usurf = np.ma.masked_where(thk < 1, usurf)
    return _contours(usurf,
      levels     = kwargs.pop('levels', range(1000, 5000, 1000)),
      linecolors = kwargs.pop('linecolors', 'black'),
      linewidths = kwargs.pop('linewidths', 0.5))

def bedtempcontour(nc, t=0, **kwargs):
    """Draw pressure-adjusted bed temperature contours"""
    thk   = _extract(nc, 'thk', t)
    temp  = _extract(nc, 'temppabase', t)
    temp  = np.ma.masked_where(thk < 1, temp)
    return _contours(temp,
      levels     = kwargs.pop('levels', [-10, -8, -6, -4, -2, -1e-6]),
      cmap       = kwargs.pop('cmap', mplt.cm.Blues_r),
      extend     = kwargs.pop('extend', 'both'),
      linewidths = kwargs.pop('linewidths', 0.2),
      linecolors = kwargs.pop('linecolors', 'black'),
      linestyles = kwargs.pop('linestyles', 'solid'),
      **kwargs)

### Quiver mapping functions ###

def bedvelquiver(nc, t=0):
    """Draw basal velocity quiver"""
    uvel  = _extract(nc, 'uvelbase', t)
    vvel  = _extract(nc, 'vvelbase', t)
    cbase = _extract(nc, 'cbase', t)
    uvel  = np.sign(uvel)*np.log(1+np.abs(uvel)/100)
    vvel  = np.sign(vvel)*np.log(1+np.abs(vvel)/100)
    cbase = np.ma.masked_less(cbase, 1)
    return mplt.quiver(uvel, vvel, cbase,
      cmap = icm.velocity,
      norm = mcolors.LogNorm(10, 10000))

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
        for kw in ('levels', 'linecolors') if 'surftopo_'+kw in kwargs})

    # draw ice margin contour
    icemargincontour(nc, t)

    # return surface velocity image
    return im

def bedtempmap(nc, t=0, **kwargs):
    """Draw basal pressure-adjusted temperature map"""

    # draw bed temperature contour
    cs = bedtempcontour(nc, t, **kwargs)

    # draw ice margin contour
    icemargincontour(nc, t)

    # return bed temperature contours
    return cs

def bedvelmap(nc, t=0):
    """Draw basal velocity map"""

    # draw bed temperature contour
    bedtempcontour(nc, t)

    # draw bed velocity quiver
    qv = bedvelquiver(nc, t)

    # draw ice margin contour
    icemargincontour(nc, t)

    # return bed velocity quiver
    return qv

