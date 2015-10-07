""":mod:`iceplotlib.axes`

Provide custom classes derived from matplotlib Axes.
"""

import numpy as np
from matplotlib.axes import Axes


class MapAxes(Axes):

    name = 'mapaxes'

    def __init__(self, *args, **kwargs):
        Axes.__init__(self, *args, **kwargs)
        self.set_aspect(1.0)
        self.xaxis.set_visible(False)
        self.yaxis.set_visible(False)

    # mapping methods overriding matplotlib's

    def contour(self, nc, varname, t=None, thkth=None, **kwargs):
        x, y, z = nc.extract_xyz(varname, t, thkth=thkth)
        cs = Axes.contour(self, x[:], y[:], z, **kwargs)
        return cs

    def contourf(self, nc, varname, t=None, thkth=None, **kwargs):
        x, y, z = nc.extract_xyz(varname, t, thkth=thkth)
        cs = Axes.contourf(self, x[:], y[:], z,
                           cmap=kwargs.pop('cmap', default_cmaps.get(varname)),
                           norm=kwargs.pop('norm', default_norms.get(varname)),
                           **kwargs)
        return cs

    def imshow(self, nc, varname, t=None, thkth=None, **kwargs):
        x, y, z = nc.extract_xyz(varname, t, thkth=thkth)
        w = (3*x[0]-x[1])/2
        e = (3*x[-1]-x[-2])/2
        n = (3*y[0]-y[1])/2
        s = (3*y[-1]-y[-2])/2
        im = Axes.imshow(self, z,
                         cmap=kwargs.pop('cmap', default_cmaps.get(varname)),
                         norm=kwargs.pop('norm', default_norms.get(varname)),
                         interpolation=kwargs.pop('interpolation', 'nearest'),
                         origin=kwargs.pop('origin', 'lower'),
                         extent=kwargs.pop('extent', (w, e, n, s)),
                         **kwargs)
        return im

    def quiver(self, nc, varname, t=None, thkth=None, **kwargs):
        x, y, u, v, c = nc.extract_xyuvc(varname, t, thkth=thkth)
        scale = kwargs.pop('scale', 100)
        u = np.sign(u)*np.log(1+np.abs(u)/scale)
        v = np.sign(v)*np.log(1+np.abs(v)/scale)
        return Axes.quiver(self, x, y, u, v, c,
                           scale=scale,
                           cmap=kwargs.pop('cmap', default_cmaps.get('c'+varname.lstrip('vel'))),
                           norm=kwargs.pop('norm', default_norms.get('c'+varname.lstrip('vel'))),
                           **kwargs)

    def streamplot(self, nc, varname, t=None, thkth=None, **kwargs):
        x, y, u, v, c = nc.extract_xyuvc(varname, t, thkth=thkth)
        return Axes.streamplot(self, x, y, u, v,
                               density=kwargs.pop('density', (1.0, 1.0*len(y)/len(x))),
                               color=kwargs.pop('color', c),
                               cmap=kwargs.pop('cmap', default_cmaps.get('c'+varname.lstrip('vel'))),
                               norm=kwargs.pop('norm', default_norms.get('c'+varname.lstrip('vel'))),
                               **kwargs)

    # new, specific mapping methods

    def icemargin(self, nc, t=None, thkth=None, **kwargs):
        """
        Draw a contour along the ice margin.
        """
        x = nc.variables['x'][:]
        y = nc.variables['y'][:]
        mask = nc.extract_mask(t, thkth=thkth)
        return Axes.contour(self, x, y, mask, levels=[0.5],
                            colors=kwargs.pop('colors', ['black']),
                            **kwargs)

    def icemarginf(self, nc, t=None, thkth=None, **kwargs):
        """
        Fill a contour along the ice margin.
        """
        x = nc.variables['x'][:]
        y = nc.variables['y'][:]
        mask = nc.extract_mask(t, thkth=thkth)
        return Axes.contourf(self, x, y, mask, levels=[-0.5, 0.5],
                             **kwargs)

    def shading(self, nc, varname, t=None, thkth=None,
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
        return Axes.imshow(self, (shade > 0)*shade,
                           cmap=kwargs.pop('cmap', default_cmaps.get('shading')),
                           norm=kwargs.pop('norm', default_norms.get('shading')),
                           extent=kwargs.pop('extent', (w, e, n, s)),
                           **kwargs)

    # new, composite mapping methods

    def icemap(self, nc, t=None, thkth=None, **kwargs):
        """Draw basal topography, surface velocity and elevation contours."""

        # draw bed topography
        self.imshow(nc, 'topg', t=t, thkth=thkth,
                    **{kw: kwargs['topg_'+kw]
                       for kw in ('cmap', 'norm') if 'topg_'+kw in kwargs})

        # draw surface velocities
        im = self.imshow(nc, 'velsurf_mag', t=t, thkth=thkth,
                         **{kw: kwargs['velsurf_'+kw]
                            for kw in ('cmap', 'norm') if 'velsurf_'+kw in kwargs})

        # draw surface topography contours
        self.contour(nc, 'usurf', t=t, thkth=thkth,
                     **{kw: kwargs['usurf_'+kw]
                        for kw in ('levels', 'cmap', 'colors') if 'usurf_'+kw in kwargs})

        # draw ice margin contour
        self.icemargin(nc, t=t, thkth=thkth)

        # return surface velocity image
        return im
