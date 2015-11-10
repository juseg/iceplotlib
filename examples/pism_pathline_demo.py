"""
Draw a streamline and a pathline.
"""

import iceplotlib.plot as iplt
from iceplotlib.flowlines import streamline, pathline

# load data
nc = iplt.load('pism_anim_sample.nc')

# parameters
t = -20e3
origin = (-1800e3, 500e3)
thkth = 1.0

# plot background map
iplt.icemap(nc, t=t, thkth=thkth, velsurf_cmap='CMRmap_r',
            usurf_cmap=None, usurf_colors='k')

# plot streamline
times, positions = streamline(nc, 'velsurf', t=t, thkth=1.0, origin=origin,
                              dt=10.0, n=501)
iplt.plot(positions[:,0], positions[:,1], 'b.-')

# plot pathline (trajectory)
times, positions = pathline(nc, 'velsurf', t=t, thkth=1.0, origin=origin,
                            dt=10.0, n=501)
iplt.plot(positions[:,0], positions[:,1], 'r.-')

# set limits to hide streamline exiting the frame
iplt.xlim(-2.5e6, -1e6)
iplt.ylim(0e6, 3e6)

# show
nc.close()
iplt.show()
