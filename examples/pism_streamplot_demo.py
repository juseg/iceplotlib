"""
Plot surface velocity streamlines.
"""

import iceplotlib.plot as iplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
iplt.axes(projection='mapaxes')
iplt.streamplot(nc, 'velsurf', thkth=1.0)
iplt.icemargin(nc, thkth=1.0)

# show
nc.close()
iplt.show()
