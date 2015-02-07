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

def _extract_2d(nc, varname, t):
    """Extract two-dimensional array from a netcdf variable."""
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
      z = var[:].squeeze()
    else:
      z = var[t]
    return z.T

def _extract_mask(nc, t, thkth=None):
    """Extract ice-cover mask from a netcdf file."""
    t = t or 0  # if t is None use first time slice
    if thkth is not None:
        mask = _extract_2d(nc, 'thk', t)
        mask = (mask < thkth)
    else:
        mask = _extract_2d(nc, 'mask', t)
        mask = (mask == 0) + (mask == 4)
    return mask

def _extract_xyuvc(nc, varname, t, thkth=None):
    """Extract coordinates and vector field from a netcdf file."""
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    u = _extract_2d(nc, 'u'+varname, t)
    v = _extract_2d(nc, 'v'+varname, t)
    mask = _extract_mask(nc, t, thkth=thkth)
    u = np.ma.masked_where(mask, u)
    v = np.ma.masked_where(mask, v)
    for cname in ['c'+varname.lstrip('vel'), varname+'_mag']:
        if cname in nc.variables:
            c = _extract_2d(nc, cname, t)
            break
    else:
        c = (u**2 + v**2)**0.5
    return x, y, u, v, c

def _extract_xyz(nc, varname, t, thkth=None):
    """Extract coordinates and scalar field from a netcdf file."""
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    z = _extract_2d(nc, varname, t)
    if varname not in ('mask', 'topg'):
        mask = _extract_mask(nc, t, thkth=thkth)
        z = np.ma.masked_where(mask, z)
    return x, y, z

### Generic mapping functions ###

def contour(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, z = _extract_xyz(nc, varname, t, thkth=thkth)
    ax = ax or gca()
    cs = ax.contour(x[:], y[:], z,
        **kwargs)
    return cs

def contourf(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, z = _extract_xyz(nc, varname, t, thkth=thkth)
    ax = ax or gca()
    cs = ax.contourf(x[:], y[:], z,
        cmap = kwargs.pop('cmap', default_cmaps.get(varname)),
        norm = kwargs.pop('norm', default_norms.get(varname)),
        **kwargs)
    return cs

def imshow(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, z = _extract_xyz(nc, varname, t, thkth=thkth)
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2
    ax = ax or gca()
    im = ax.imshow(z,
      cmap = kwargs.pop('cmap', default_cmaps.get(varname)),
      norm = kwargs.pop('norm', default_norms.get(varname)),
      extent = kwargs.pop('extent', (w, e, n, s)),
      **kwargs)
    return im

def shading(nc, varname, t=None, ax=None, thkth=None,
            azimuth=315, altitude=0, **kwargs):

    # extract data
    x, y, z = _extract_xyz(nc, varname, t, thkth=thkth)
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
    cmap = mcolors.LinearSegmentedColormap.from_list('shadow', [
        (0.0, (0,0,0,0)),
        (1.0, (0,0,0,1))])
    return ax.imshow((shade>0)*shade, cmap=cmap,
      norm=kwargs.pop('norm', mcolors.Normalize(0, 1)),
      extent = kwargs.pop('extent', (w, e, n, s)),
      **kwargs)

def quiver(nc, varname, t=None, ax=None, thkth=None, **kwargs):
    x, y, u, v, c = _extract_xyuvc(nc, varname, t, thkth=thkth)
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
    x, y, u, v, c = _extract_xyuvc(nc, varname, t, thkth=thkth)
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
    mask = _extract_mask(nc, t, thkth=thkth)
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
    mask = _extract_mask(nc, t, thkth=thkth)
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
    icemargin(nc, t=t, ax=ax)

    # return surface velocity image
    return im
