"""
Draw a streamline and a pathline.
"""

from matplotlib import pyplot as plt
from iceplotlib import autoplot as aplt
from iceplotlib.flowlines import streamline, pathline

# load data
nc = aplt.load('pism_anim_sample.nc')

# parameters
t = -20e3
origin = (-1800e3, 500e3)
thkth = 1.0

# locate time index
# FIXME this should be done in _extract for all plots
import numpy as np
s2yr = 1/(365.0 * 24 * 60 * 60)
time = nc.variables['time'][:]*s2yr
tidx = np.argmin(np.abs(time-t))

# plot background map
aplt.icemap(nc, t=tidx, thkth=thkth, velsurf_cmap='CMRmap_r',
            usurf_cmap=None, usurf_colors='k')

# plot streamline
times, positions = streamline(nc, 'velsurf', t=t, thkth=1.0, origin=origin,
                              dt=10.0, n=501)
plt.plot(positions[:,0], positions[:,1], 'b.-')

# plot pathline (trajectory)
times, positions = pathline(nc, 'velsurf', t=t, thkth=1.0, origin=origin,
                            dt=10.0, n=501)
plt.plot(positions[:,0], positions[:,1], 'r.-')

# set limits to hide streamline exiting the frame
plt.xlim(-2.5e6, -1e6)
plt.ylim(0e6, 3e6)

# show
nc.close()
plt.show()
