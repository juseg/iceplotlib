""":mod:`iceplotlib.flowlines`

Compute various types of flowlines.
"""

import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import RegularGridInterpolator
from iceplotlib.plot import _extract_xyuvc


def pathline(nc, varname, origin, t=None, dt=10.0, n=101,
               thkth=None, **kwargs):

    # extract 3d data
    # FIXME move this somewhere else
    s2yr = 1/(365.0 * 24 * 60 * 60)
    time = nc.variables['time'][:]*s2yr
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    u = nc.variables['uvelsurf'][:]
    v = nc.variables['vvelsurf'][:]

    # build spatial interpolators
    u_interp = RegularGridInterpolator((time, x, y), u, bounds_error=False)
    v_interp = RegularGridInterpolator((time, x, y), v, bounds_error=False)
    vel_interp = lambda t, pos: np.hstack((u_interp((t, pos[0], pos[1])),
                                           v_interp((t, pos[0], pos[1]))))

    # initialize output
    dates = t + dt*np.arange(n)
    positions = np.zeros((n, 2))
    positions[0] = origin

    # integrate by RK4 method
    for i, t in enumerate(dates[:-1]):
        pos = positions[i]
        k1 = vel_interp(t, pos)
        k2 = vel_interp(t + 0.5*dt, pos + 0.5*dt*k1)
        k3 = vel_interp(t + 0.5*dt, pos + 0.5*dt*k2)
        k4 = vel_interp(t + dt, pos + dt*k3)
        positions[i+1] = (pos + dt*(k1 + 2*k2 + 2*k3 + k4)/6)

    # return dates and positions
    return dates, positions


def streamline(nc, varname, origin, t=None, dt=10.0, n=101,
               thkth=None, **kwargs):

    # extract data
    # FIXME move this somewhere else
    s2yr = 1/(365.0 * 24 * 60 * 60)
    time = nc.variables['time'][:]*s2yr
    tidx = np.argmin(np.abs(time-t))
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    u = nc.variables['uvelsurf'][tidx]
    v = nc.variables['vvelsurf'][tidx]

    # build spatial interpolators
    u_interp = RegularGridInterpolator((x, y), u, bounds_error=False)
    v_interp = RegularGridInterpolator((x, y), v, bounds_error=False)
    vel_interp = lambda pos: np.hstack((u_interp(pos), v_interp(pos)))

    # initialize output
    dates = t + dt*np.arange(n)
    positions = np.zeros((n, 2))
    positions[0] = origin

    # integrate by RK4 method
    for i, t in enumerate(dates[:-1]):
        pos = positions[i]
        k1 = vel_interp(pos)
        k2 = vel_interp(pos + 0.5*dt*k1)
        k3 = vel_interp(pos + 0.5*dt*k2)
        k4 = vel_interp(pos + dt*k3)
        positions[i+1] = (pos + dt*(k1 + 2*k2 + 2*k3 + k4)/6)

    # return dates and positions
    return dates, positions
