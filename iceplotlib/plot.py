""":mod:`iceplotlib.plot`

Provide the actual plotting interface.
"""

import numpy as np
from matplotlib.pyplot import gca, figure
from iceplotlib.colors import default_cmaps, default_norms
from iceplotlib.figure import GridFigure, SimpleFigure, DoubleInlineFigure

### File open function ###
def load(filename):
    from iceplotlib.io import IceDataset
    return IceDataset(filename)

### Figure functions ###

def gridfigure(mapsize, nrows_ncols, **kwargs):
    """Create a new figure and return an :class:iceplotlib.figure.GridFigure instance"""
    return figure(FigureClass=GridFigure,
      mapsize=mapsize, nrows_ncols=nrows_ncols, **kwargs)

def simplefigure(mapsize, **kwargs):
    """Create a new figure and return a :class:iceplotlib.figure.SimpleFigure instance"""
    return figure(FigureClass=SimpleFigure,
      mapsize=mapsize, **kwargs)

def doubleinlinefigure(mapsize, **kwargs):
    """Create a new figure and return a :class:iceplotlib.figure.DoubleInlineFigure instance"""
    return figure(FigureClass=DoubleInlineFigure,
      mapsize=mapsize, **kwargs)

### Generic mapping functions ###

def contour(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, z = nc.extract_xyz(varname, t, thkth=thkth)
    ax = ax or gca()
    cs = ax.contour(x[:], y[:], z,
        **kwargs)
    return cs

def contourf(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, z = nc.extract_xyz(varname, t, thkth=thkth)
    ax = ax or gca()
    cs = ax.contourf(x[:], y[:], z,
        cmap = kwargs.pop('cmap', default_cmaps.get(varname)),
        norm = kwargs.pop('norm', default_norms.get(varname)),
        **kwargs)
    return cs

def imshow(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, z = nc.extract_xyz(varname, t, thkth=thkth)
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2
    ax = ax or gca()
    im = ax.imshow(z,
      cmap = kwargs.pop('cmap', default_cmaps.get(varname)),
      norm = kwargs.pop('norm', default_norms.get(varname)),
      interpolation=kwargs.pop('interpolation', 'nearest'),
      origin = kwargs.pop('origin', 'lower'),
      extent = kwargs.pop('extent', (w, e, n, s)),
      **kwargs)
    return im

def shading(nc, varname, t=None, ax=None, thkth=None,
            azimuth=315, altitude=0, **kwargs):

    # extract data
    x, y, z = nc.extract_xyz(varname, t, thkth=thkth)
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2

    # convert to rad from the x-axis
    azimuth = (90-azimuth)*np.pi / 180.
    altitude = altitude*np.pi / 180.

    # compute cartesian coords of the illumination direction
    x0 = np.cos(azimuth) * np.cos(altitude)
    y0 = np.sin(azimuth) * np.cos(altitude)
    z0 = np.sin(altitude)
    z0 = 0.0  # remove shades from horizontal surfaces

    # compute hillshade (dot product of normal and light direction vectors)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    u, v = np.gradient(z, dx, dy)
    shade = (z0 - u*x0 - v*y0) / (1 + u**2 + v**2)**(0.5)

    # plot shadows only (white transparency is not possible)
    ax = ax or gca()
    return ax.imshow((shade>0)*shade,
      cmap = kwargs.pop('cmap', default_cmaps.get('shading')),
      norm = kwargs.pop('norm', default_norms.get('shading')),
      extent = kwargs.pop('extent', (w, e, n, s)),
      **kwargs)

def quiver(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, u, v, c = nc.extract_xyuvc(varname, t, thkth=thkth)
    scale = kwargs.pop('scale', 100)
    u = np.sign(u)*np.log(1+np.abs(u)/scale)
    v = np.sign(v)*np.log(1+np.abs(v)/scale)
    ax = ax or gca()
    return ax.quiver(x, y, u, v, c,
      scale = scale,
      cmap = kwargs.pop('cmap', default_cmaps.get('c'+varname.lstrip('vel'))),
      norm = kwargs.pop('norm', default_norms.get('c'+varname.lstrip('vel'))),
      **kwargs)

def streamplot(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, u, v, c = nc.extract_xyuvc(varname, t, thkth=thkth)
    ax = ax or gca()
    return ax.streamplot(x, y, u, v,
      density = kwargs.pop('density', (1.0, 1.0*len(y)/len(x))),
      color   = kwargs.pop('color', c),
      cmap = kwargs.pop('cmap', default_cmaps.get('c'+varname.lstrip('vel'))),
      norm = kwargs.pop('norm', default_norms.get('c'+varname.lstrip('vel'))),
      **kwargs)

### Specific mapping functions ###

def icemargin(nc, t=None, ax=None, thkth=None, **kwargs):
    """
    Draw a contour along the ice margin.
    """
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    mask = nc.extract_mask(t, thkth=thkth)
    ax = ax or gca()
    return ax.contour(x, y, mask, levels=[0.5],
                      colors = kwargs.pop('colors', ['black']),
                      **kwargs)

def icemarginf(nc, t=None, ax=None, thkth=None, **kwargs):
    """
    Fill a contour along the ice margin.
    """
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    mask = nc.extract_mask(t, thkth=thkth)
    ax = ax or gca()
    return ax.contourf(x, y, mask, levels=[-0.5, 0.5],
                      **kwargs)

### Composite mapping functions ###

def icemap(nc, t=None, ax=None, thkth=None, **kwargs):
    """Draw basal topography, surface velocity and elevation contours."""

    # draw bed topography
    imshow(nc, 'topg', t=t, ax=ax, thkth=thkth,
      **{kw: kwargs['topg_'+kw]
        for kw in ('cmap', 'norm') if 'topg_'+kw in kwargs})

    # draw surface velocities
    im = imshow(nc, 'velsurf_mag', t=t, ax=ax, thkth=thkth,
      **{kw: kwargs['velsurf_'+kw]
        for kw in ('cmap', 'norm') if 'velsurf_'+kw in kwargs})

    # draw surface topography contours
    contour(nc, 'usurf', t=t, ax=ax, thkth=thkth,
      **{kw: kwargs['usurf_'+kw]
        for kw in ('levels', 'cmap', 'colors') if 'usurf_'+kw in kwargs})

    # draw ice margin contour
    icemargin(nc, t=t, ax=ax, thkth=thkth)

    # return surface velocity image
    return im
