"""
Draw the module's canonical icemap.
"""

import iceplotlib.plot as iplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
iplt.axes(projection='mapaxes')
iplt.icemap(nc, thkth=1.0, velsurf_cmap='CMRmap_r',
            usurf_cmap=None, usurf_colors='k')

# show
nc.close()
iplt.show()
