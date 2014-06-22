""":mod:`iceplot.plot`

Provide the actual plotting interface
"""

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from matplotlib.pyplot import gca
from matplotlib import colors as mcolors

from iceplot.colors import default_cmaps, default_norms
from iceplot import figure as ifig

### Figure functions ###

def gridfigure(mapsize, nrows_ncols, **kwargs):
    """Create a new figure and return an :class:iceplot.figure.GridFigure instance"""
    return mplt.figure(FigureClass=ifig.GridFigure,
      mapsize=mapsize, nrows_ncols=nrows_ncols, **kwargs)

def simplefigure(mapsize, **kwargs):
    """Create a new figure and return a :class:iceplot.figure.SimpleFigure instance"""
    return mplt.figure(FigureClass=ifig.SimpleFigure,
      mapsize=mapsize, **kwargs)

def doubleinlinefigure(mapsize, **kwargs):
    """Create a new figure and return a :class:iceplot.figure.DoubleInlineFigure instance"""
    return mplt.figure(FigureClass=ifig.DoubleInlineFigure,
      mapsize=mapsize, **kwargs)

### Data extraction ###

def _extract(nc, varname, t):
    """Extract data from a netcdf file"""
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    z = _oldextract(nc, varname, t)
    if varname not in ('mask', 'topg'):
        mask = nc.variables['mask'][t].T
        icefree = (mask == 0) + (mask == 4)
        z = np.ma.masked_where(icefree, z)
    return x, y, z


def _oldextract(nc, varname, t):
    """Extract data from a netcdf file"""
    var = nc.variables[varname]

    if t == 'djf':
      z = var[[12,0,1]].mean(axis=2)
    elif t == 'mam':
      z = var[2:5].mean(axis=2)
    elif t == 'jja':
      z = var[6:8].mean(axis=2)
    elif t == 'son':
      z = var[9:11].mean(axis=2)
    elif t == 'mean':
      z = var[:].mean(axis=2)
    elif t is None:
      z = var[:]
    else:
      z = var[t]
    return z.T

### Generic mapping functions ###

def contour(nc, varname, t=None, **kwargs):
    x, y, z = _extract(nc, varname, t)
    ax = gca()
    cs = ax.contour(x[:], y[:], z,
        cmap = kwargs.pop('cmap', default_cmaps.get(varname)),
        norm = kwargs.pop('norm', default_norms.get(varname)),
        **kwargs)
    return cs

def contourf(nc, varname, t=None, **kwargs):
    x, y, z = _extract(nc, varname, t)
    ax = gca()
    cs = ax.contourf(x[:], y[:], z,
        cmap = kwargs.pop('cmap', default_cmaps.get(varname)),
        norm = kwargs.pop('norm', default_norms.get(varname)),
        **kwargs)
    return cs

def imshow(nc, varname, t=None, **kwargs):
    x, y, z = _extract(nc, varname, t)
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2
    ax = gca()
    im = ax.imshow(z,
      cmap = kwargs.pop('cmap', default_cmaps.get(varname)),
      norm = kwargs.pop('norm', default_norms.get(varname)),
      extent = kwargs.pop('extent', (w, e, n, s)),
      **kwargs)
    return im

### Specific mapping functions ###

def icemargin(nc, t=None, **kwargs):
    """
    Draw a contour along the ice margin.
    """
    x, y, mask = _extract(nc, 'mask', t)
    icy = (mask == 1) + (mask == 2)
    ax = gca()
    return ax.contour(x, y, icy, levels=[0.5],
                      colors = kwargs.pop('colors', ['black']),
                      **kwargs)


### Image mapping functions ###

def bedtopoimage(nc, t=0, **kwargs):
    """
    Draw bedrock topography map using :func:`matplotlib.pyplot.imshow`.

    Keyword arguments:

      *cmap*: [ *None* | Colormap ]
        A :class:`matplotlib.colors.Colormap` instance. If *None*,
        a default Wikipedia-based colormap is used.
      *norm*: [ *None* | Normalize ]
        A :class:`matplotlib.colors.Normalize` instance. If *None*,
        luminance is scaled linearly between -6000 and 6000 m.

    See :func:`matplotlib.pyplot.imshow` for complete documentation.
    """
    topo = _oldextract(nc, 'topg', t)
    return mplt.imshow(topo,
      cmap = kwargs.pop('cmap', default_cmaps['topg']),
      norm = kwargs.pop('norm', default_norms['topg']),
      **kwargs)

def surftopoimage(nc, t=0, **kwargs):
    """
    Draw ice surface topography map using :func:`matplotlib.pyplot.imshow`.

    Keyword arguments:

      *cmap*: [ *None* | Colormap ]
        A :class:`matplotlib.colors.Colormap` instance. If *None*,
        a default Wikipedia-based colormap is used.
      *norm*: [ *None* | Normalize ]
        A :class:`matplotlib.colors.Normalize` instance. If *None*,
        luminance is scaled linearly between 0 and 6000 m.

    See :func:`matplotlib.pyplot.imshow` for complete documentation.
    """
    topo = _oldextract(nc, 'usurf', t)
    return mplt.imshow(topo,
      cmap = kwargs.pop('cmap', default_cmaps['usurf']),
      norm = kwargs.pop('norm', default_norms['topg']),
      **kwargs)

def basetempimage(nc, t=0, **kwargs):
    """
    Draw a map of basal temperature above melting point using
    :func:`matplotlib.pyplot.imshow`.

    Keyword arguments:

      *cmap*: [ *None* | Colormap ]
        A :class:`matplotlib.colors.Colormap` instance. If *None*,
        :data:`matplotlib.cm.Blues_r` is used.
      *norm*: [ *None* | Normalize ]
        A :class:`matplotlib.colors.Normalize` instance. If *None*,
        luminance is scaled linearly between -10 and 0 K.

    See :func:`matplotlib.pyplot.imshow` for complete documentation.
    """
    thk   = _oldextract(nc, 'thk', t)
    temp  = _oldextract(nc, 'temppabase', t)
    temp  = np.ma.masked_where(thk < 1, temp)
    return mplt.imshow(temp,
      cmap = kwargs.pop('cmap', default_cmaps['temppabase']),
      norm = kwargs.pop('norm', default_norms['temppabase']),
      **kwargs)

def airtempimage(nc, t=0, **kwargs):
    """
    Draw surface air temperature map using
    :func:`matplotlib.pyplot.imshow`.

    Keyword arguments:

      *cmap*: [ *None* | Colormap ]
        A :class:`matplotlib.colors.Colormap` instance. If *None*,
        :data:`matplotlib.cm.Spectral_r` is used.
      *norm*: [ *None* | Normalize ]
        A :class:`matplotlib.colors.Normalize` instance. If *None*,
        luminance is scaled linearly between -30 and 30 degree C.

    See :func:`matplotlib.pyplot.imshow` for complete documentation.
    """
    temp = _oldextract(nc, 'air_temp', t)
    return mplt.imshow(temp,
      cmap = kwargs.pop('cmap', default_cmaps['air_temp']),
      norm = kwargs.pop('norm', default_norms['air_temp']),
      **kwargs)

def precipimage(nc, t=0, **kwargs):
    """
    Draw precipitation rate map using :func:`matplotlib.pyplot.imshow`.

    Keyword arguments:

      *cmap*: [ *None* | Colormap ]
        A :class:`matplotlib.colors.Colormap` instance. If *None*,
        :data:`matplotlib.cm.YlGnBu` is used.
      *norm*: [ *None* | Normalize ]
        A :class:`matplotlib.colors.Normalize` instance. If *None*,
        luminance is scaled logarithmically between 0.1 and 10 m yr-1.

    See :func:`matplotlib.pyplot.imshow` for complete documentation.
    """
    prec = _oldextract(nc, 'precipitation', t)
    return mplt.imshow(prec,
      cmap = kwargs.pop('cmap', default_cmaps['precipitation']),
      norm = kwargs.pop('norm', default_norms['precipitation']),
      **kwargs)

def _icevelimage(nc, t=0, surf='surf', **kwargs):
    """Draw ice velocity map."""
    thk = _oldextract(nc, 'thk', t)
    c   = _oldextract(nc, 'c'+surf, t)
    c   = np.ma.masked_where(thk < 1, c)
    return mplt.imshow(c,
      cmap = kwargs.pop('cmap', default_cmaps['c'+surf]),
      norm = kwargs.pop('norm', default_norms['c'+surf]),
      **kwargs)

def basevelimage(nc, t=0, **kwargs):
    """
    Draw basal velocity map using :func:`matplotlib.pyplot.imshow`.

    Keyword arguments:

      *cmap*: [ *None* | Colormap ]
        A :class:`matplotlib.colors.Colormap` instance. If *None*,
        a default colormap is used.
      *norm*: [ *None* | Normalize ]
        A :class:`matplotlib.colors.Normalize` instance. If *None*,
        luminance is scaled logarithmically between 10 and 10,000 m yr-1.

    See :func:`matplotlib.pyplot.imshow` for complete documentation.
    """
    return _icevelimage(nc, t, 'base', **kwargs)

def surfvelimage(nc, t=0, **kwargs):
    """
    Draw ice surface velocity map using :func:`matplotlib.pyplot.imshow`.

    Keyword arguments:

      *cmap*: [ *None* | Colormap ]
        A :class:`matplotlib.colors.Colormap` instance. If *None*,
        a default colormap is used.
      *norm*: [ *None* | Normalize ]
        A :class:`matplotlib.colors.Normalize` instance. If *None*,
        luminance is scaled logarithmically between 10 and 10,000 m yr-1.

    See :func:`matplotlib.pyplot.imshow` for complete documentation.
    """
    return _icevelimage(nc, t, 'surf', **kwargs)

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
    """
    Draw a contour along the ice margin using
    :func:`matplotlib.pyplot.contour` and
    :func:`matplotlib.pyplot.contourf`.

    Keyword arguments:

      *level*: [ *None* | scalar ]
        Thickness level used for ice margin. If *None*, a value of 1 (m)
        is used in order to ignore potential annual snow cover and
        numerical artefacts.
      *linecolor*: [ *None* | string | mpl_colors ]
        Line color. A color argument in :mod:`matplotlib` sense.
        If *None*, defaults to black.

    See :func:`matplotlib.pyplot.contour` for complete documentation.
    """
    thk = _oldextract(nc, 'thk', t)
    return _contours(thk,
      levels     = [kwargs.pop('level', 1), np.inf],
      linecolors = kwargs.pop('linecolors', 'black'),
      **kwargs)

def surftopocontour(nc, t=0, **kwargs):
    """Draw ice surface topography contours."""
    thk   = _oldextract(nc, 'thk', t)
    usurf = _oldextract(nc, 'usurf', t)
    usurf = np.ma.masked_where(thk < 1, usurf)
    return _contours(usurf,
      levels     = kwargs.pop('levels', range(1000, 5000, 1000)),
      linecolors = kwargs.pop('linecolors', 'black'),
      linewidths = kwargs.pop('linewidths', 0.5),
      **kwargs)

def basetempcontour(nc, t=0, **kwargs):
    """Draw pressure-adjusted bed temperature contours."""
    thk   = _oldextract(nc, 'thk', t)
    temp  = _oldextract(nc, 'temppabase', t)
    temp  = np.ma.masked_where(thk < 1, temp)
    return _contours(temp,
      levels     = kwargs.pop('levels', [-10, -8, -6, -4, -2, -1e-6]),
      cmap       = kwargs.pop('cmap', default_cmaps['temppabase']),
      extend     = kwargs.pop('extend', 'both'),
      linewidths = kwargs.pop('linewidths', 0.2),
      linecolors = kwargs.pop('linecolors', 'black'),
      linestyles = kwargs.pop('linestyles', 'solid'),
      **kwargs)

def airtempcontour(nc, t=0, **kwargs):
    """Draw near-surface air temperature contours using
    :func:`matplotlib.pyplot.contour` and
    :func:`matplotlib.pyplot.contourf`.

    Keyword arguments:

      *levels*: [ *None* | list ]
      *cmap*: [ *None* | Colormap ]
      *norm*: [ *None* | Normalize ]
      *linewidths*: [ *None* | number | tuple of numbers ]
      *linecolors*: [ *None* | string | (mpl_colors) ]
      *linestyles*: [ *None* | 'solid' | 'dashed' | 'dashdot' | 'dotted' ]

      *cmap*: [ *None* | Colormap ]
        A :class:`matplotlib.colors.Colormap` instance. If *None*,
        a default Wikipedia-based colormap is used.
      *norm*: [ *None* | Normalize ]
        A :class:`matplotlib.colors.Normalize` instance. If *None*,
        luminance is scaled linearly between -6000 and 6000 m.

    See :func:`matplotlib.pyplot.imshow` for complete documentation.
    """
    temp = _oldextract(nc, 'air_temp', t) - 273.15
    return _contours(temp,
      levels     = kwargs.pop('levels', range(-30, 31, 5)),
      cmap       = kwargs.pop('cmap', default_cmaps['air_temp']),
      norm       = kwargs.pop('norm', default_norms['air_temp']),
      linewidths = kwargs.pop('linewidths', 0.2),
      linecolors = kwargs.pop('linecolors', 'black'),
      linestyles = kwargs.pop('linestyles', 'solid'),
      **kwargs)

def precipcontour(nc, t=0, **kwargs):
    """Draw precipitation rate contours."""
    prec = _oldextract(nc, 'precipitation', t)
    return _contours(prec,
      levels     = kwargs.pop('levels', [0.1, 0.2, 0.5, 1, 2, 5, 10]),
      cmap       = kwargs.pop('cmap', default_cmaps['precipitation']),
      norm       = kwargs.pop('norm', default_norms['precipitation']),
      linewidths = kwargs.pop('linewidths', 0.2),
      linecolors = kwargs.pop('linecolors', 'black'),
      **kwargs)

def _icevelcontour(nc, t=0, surf='surf', **kwargs):
    """Draw ice velocity contours."""
    thk = _oldextract(nc, 'thk', t)
    c   = _oldextract(nc, 'c'+surf, t)
    c   = np.ma.masked_where(thk < 1, c)
    return _contours(c,
      levels     = kwargs.pop('levels', [10,30,100,300,1000,3000,10000]),
      cmap       = kwargs.pop('cmap', default_cmaps['c'+surf]),
      norm       = kwargs.pop('norm', default_norms['c'+surf]),
      linewidths = kwargs.pop('linewidths', 0.2),
      linecolors = kwargs.pop('linecolors', 'black'),
      **kwargs)

def basevelcontour(nc, t=0, **kwargs):
    """Draw basal velocity contours."""
    return _icevelcontour(nc, t, 'base', **kwargs)

def surfvelcontour(nc, t=0, **kwargs):
    """Draw surface velocity contours."""
    return _icevelcontour(nc, t, 'surf', **kwargs)

### Quiver mapping functions ###

def _icevelquiver(nc, t=0, surf='surf', **kwargs):
    """Draw ice velocity quiver"""
    thk = _oldextract(nc, 'thk', t)
    u = _oldextract(nc, 'uvel'+surf, t)
    v = _oldextract(nc, 'vvel'+surf, t)
    try:
      c = _oldextract(nc, 'c'+surf, t)
    except KeyError:
      c = (u**2 + v**2)**0.5
    scale = kwargs.pop('scale', 100)
    u = np.sign(u)*np.log(1+np.abs(u)/scale)
    v = np.sign(v)*np.log(1+np.abs(v)/scale)
    u = np.ma.masked_where(thk < 1, u)
    v = np.ma.masked_where(thk < 1, v)
    return mplt.quiver(u, v, c,
      scale = scale,
      cmap = kwargs.pop('cmap', icm.velocity),
      norm = kwargs.pop('norm', mcolors.LogNorm(10, 10000)),
      **kwargs)

def basevelquiver(nc, t=0, **kwargs):
    """Draw basal velocity quiver"""
    return _icevelquiver(nc, t, 'base', **kwargs)

def surfvelquiver(nc, t=0, **kwargs):
    """Draw basal velocity quiver"""
    return _icevelquiver(nc, t, 'surf', **kwargs)

### Streamplot mapping functions ###

def _icevelstreamplot(nc, t=0, surf='surf', **kwargs):
    """Draw ice velocity quiver"""
    x = np.arange(len(nc.dimensions['x']))
    y = np.arange(len(nc.dimensions['y']))
    thk = _oldextract(nc, 'thk', t)
    u = _oldextract(nc, 'uvel'+surf, t)
    v = _oldextract(nc, 'vvel'+surf, t)
    c = _oldextract(nc, 'c'+surf, t)
    u = np.ma.masked_where(thk < 1, u)
    v = np.ma.masked_where(thk < 1, v)
    return mplt.streamplot(x, y, u, v,
      linewidth = kwargs.pop('linewidths', 0.5),
      color     = kwargs.pop('color', c),
      cmap      = kwargs.pop('cmap', default_cmaps['c'+surf]),
      norm      = kwargs.pop('norm', default_norms['c'+surf]),
      **kwargs)

def basevelstreamplot(nc, t=0, **kwargs):
    """Draw basal velocity quiver"""
    return _icevelstreamplot(nc, t, 'base', **kwargs)

def surfvelstreamplot(nc, t=0, **kwargs):
    """Draw basal velocity quiver"""
    return _icevelstreamplot(nc, t, 'surf', **kwargs)

### Composite mapping functions ###

def icemap(nc, t=None, **kwargs):
    """Draw basal topography, surface velocity and elevation contours.

    **Example:**

    .. plot:: ../examples/pism_icemap_demo.py
    """

    # draw bed topography
    imshow(nc, 'topg', t=t,
      **{kw: kwargs['topg_'+kw]
        for kw in ('cmap', 'norm') if 'topg_'+kw in kwargs})

    # draw surface velocities
    im = imshow(nc, 'velsurf_mag', t=t,
      **{kw: kwargs['velsurf_'+kw]
        for kw in ('cmap', 'norm') if 'velsurf_'+kw in kwargs})

    # draw surface topography contours
    contour(nc, 'usurf', t=t,
      **{kw: kwargs['usurf_'+kw]
        for kw in ('levels', 'cmap', 'colors') if 'usurf_'+kw in kwargs})

    # draw ice margin contour
    icemargin(nc, t=t)

    # return surface velocity image
    return im
