""":mod:`iceplotlib.io`

Provide an interface to PISM NetCDF files.
"""

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset, MFDataset
from iceplotlib.colors import default_cmaps, default_norms

# convert seconds to year
# FIXME: perform conversion using UDUnits instead
yr2s = 365.0 * 24 * 60 * 60


def _get_map_axes(ax=None):
    ax = ax or plt.gca()
    ax.set_aspect(1.0)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    return ax


class IceDataset(Dataset):
    """NetCDF Dataset with plotting methods."""

    def __init__(self, filename, thkth=1.0, **kwargs):
        Dataset.__init__(self, filename, **kwargs)
        self.__dict__['thkth'] = thkth

    # data extraction methods

    def _extract_2d(self, varname, t):
        """Extract two-dimensional array from a netcdf variable."""
        var = self.variables[varname]
        time = self.variables['time']
        if t == 'djf':
            z = var[[12, 0, 1]].mean(axis=2)
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
            tidx = ((time[:]-t*yr2s)**2).argmin()
            z = var[tidx]
        if var.dimensions[-2:] == ('x', 'y'):
            z = z.T
        return z

    def _extract_mask(self, t, thkth=None):
        """Extract ice-cover mask from a netcdf file."""
        t = t or 0  # if t is None use first time slice
        thkth = thkth or self.thkth
        if thkth is not None and 'thk' in self.variables:
            mask = self._extract_2d('thk', t)
            mask = (mask < thkth)
        elif 'mask' in self.variables:
            mask = self._extract_2d('mask', t)
            mask = (mask == 0) + (mask == 4)
        else:
            mask = None
        return mask

    def _extract_xyuvc(self, varname, t, thkth=None):
        """Extract coordinates and vector field from a netcdf file."""
        x = self.variables['x'][:]
        y = self.variables['y'][:]
        u = self._extract_2d('u'+varname, t)
        v = self._extract_2d('v'+varname, t)
        mask = self._extract_mask(t, thkth=thkth)
        u = np.ma.masked_where(mask, u)
        v = np.ma.masked_where(mask, v)
        for cname in ['c'+varname.lstrip('vel'), varname+'_mag']:
            if cname in self.variables:
                c = self._extract_2d(cname, t)
                break
        else:
            c = (u**2 + v**2)**0.5
        return x, y, u, v, c

    def _extract_xyz(self, varname, t, thkth=None):
        """Extract coordinates and scalar field from a netcdf file."""
        x = self.variables['x'][:]
        y = self.variables['y'][:]
        z = self._extract_2d(varname, t)
        if varname not in ('mask', 'topg'):
            mask = self._extract_mask(t, thkth=thkth)
            z = np.ma.masked_where(mask, z)
        return x, y, z

    # map-plane plotting methods

    def contour(self, varname, ax=None, t=None, thkth=None, **kwargs):
        ax = _get_map_axes(ax)
        x, y, z = self._extract_xyz(varname, t, thkth=thkth)
        cs = ax.contour(x[:], y[:], z, **kwargs)
        return cs

    def contourf(self, varname, ax=None, t=None, thkth=None, **kwargs):
        ax = _get_map_axes(ax)
        x, y, z = self._extract_xyz(varname, t, thkth=thkth)
        cs = ax.contourf(x[:], y[:], z,
                         cmap=kwargs.pop('cmap', default_cmaps.get(varname)),
                         norm=kwargs.pop('norm', default_norms.get(varname)),
                         **kwargs)
        return cs

    def imshow(self, varname, ax=None, t=None, thkth=None, **kwargs):
        ax = _get_map_axes(ax)
        x, y, z = self._extract_xyz(varname, t, thkth=thkth)
        w = (3*x[0]-x[1])/2
        e = (3*x[-1]-x[-2])/2
        n = (3*y[0]-y[1])/2
        s = (3*y[-1]-y[-2])/2
        im = ax.imshow(z,
                       cmap=kwargs.pop('cmap', default_cmaps.get(varname)),
                       norm=kwargs.pop('norm', default_norms.get(varname)),
                       interpolation=kwargs.pop('interpolation', 'nearest'),
                       origin=kwargs.pop('origin', 'lower'),
                       extent=kwargs.pop('extent', (w, e, n, s)),
                       **kwargs)
        return im

    def quiver(self, varname, ax=None, t=None, thkth=None, **kwargs):
        ax = _get_map_axes(ax)
        x, y, u, v, c = self._extract_xyuvc(varname, t, thkth=thkth)
        scale = kwargs.pop('scale', 100)
        u = np.sign(u)*np.log(1+np.abs(u)/scale)
        v = np.sign(v)*np.log(1+np.abs(v)/scale)
        return ax.quiver(x, y, u, v, c, scale=scale,
                         cmap=kwargs.pop('cmap', default_cmaps.get(
                            'c'+varname.lstrip('vel'))),
                         norm=kwargs.pop('norm', default_norms.get(
                            'c'+varname.lstrip('vel'))),
                         **kwargs)

    def streamplot(self, varname, ax=None, t=None, thkth=None, **kwargs):
        ax = _get_map_axes(ax)
        x, y, u, v, c = self._extract_xyuvc(varname, t, thkth=thkth)
        return ax.streamplot(x, y, u, v,
                             density=kwargs.pop('density',
                                                (1.0, 1.0*len(y)/len(x))),
                             color=kwargs.pop('color', c),
                             cmap=kwargs.pop('cmap', default_cmaps.get(
                                'c'+varname.lstrip('vel'))),
                             norm=kwargs.pop('norm', default_norms.get(
                                'c'+varname.lstrip('vel'))),
                             **kwargs)

    def icemargin(self, ax=None, t=None, thkth=None, **kwargs):
        """
        Draw a contour along the ice margin.
        """
        ax = _get_map_axes(ax)
        x = self.variables['x'][:]
        y = self.variables['y'][:]
        mask = self._extract_mask(t, thkth=thkth)
        return ax.contour(x, y, mask, levels=[0.5],
                          colors=kwargs.pop('colors', ['black']),
                          **kwargs)

    def icemarginf(self, ax=None, t=None, thkth=None, **kwargs):
        """
        Fill a contour along the ice margin.
        """
        ax = _get_map_axes(ax)
        x = self.variables['x'][:]
        y = self.variables['y'][:]
        mask = self._extract_mask(t, thkth=thkth)
        return ax.contourf(x, y, mask, levels=[-0.5, 0.5],
                           **kwargs)

    def shading(self, varname, ax=None, t=None, thkth=None,
                azimuth=315, altitude=0, **kwargs):

        # extract data
        x, y, z = self._extract_xyz(varname, t, thkth=thkth)
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
        ax = _get_map_axes(ax)
        return ax.imshow((shade > 0)*shade,
                         cmap=kwargs.pop('cmap', default_cmaps.get('shading')),
                         norm=kwargs.pop('norm', default_norms.get('shading')),
                         extent=kwargs.pop('extent', (w, e, n, s)),
                         **kwargs)

    # new, composite mapping methods

    def icemap(self, ax=None, t=None, thkth=None, **kwargs):
        """Draw basal topography, surface velocity and elevation contours."""
        ax = _get_map_axes(ax)

        # draw bed topography
        self.imshow('topg', ax=ax, t=t, thkth=thkth,
                    **{kw: kwargs['topg_'+kw]
                       for kw in ('cmap', 'norm') if 'topg_'+kw in kwargs})

        # draw surface velocities
        im = self.imshow('velsurf_mag', ax=ax, t=t, thkth=thkth,
                         **{kw: kwargs['velsurf_'+kw]
                            for kw in ('cmap', 'norm') if 'velsurf_'+kw in kwargs})

        # draw surface topography contours
        self.contour('usurf', ax=ax, t=t, thkth=thkth,
                     **{kw: kwargs['usurf_'+kw]
                        for kw in ('levels', 'cmap', 'colors') if 'usurf_'+kw in kwargs})

        # draw ice margin contour
        self.icemargin(t=t, ax=ax, thkth=thkth)

        # return surface velocity image
        return im

class MFIceDataset(IceDataset, MFDataset):
    """Multi-file NetCDF Dataset with plotting methods."""

    def __init__(self, files, thkth=1.0, **kwargs):
        MFDataset.__init__(self, files, **kwargs)
        self.__dict__['thkth'] = thkth
