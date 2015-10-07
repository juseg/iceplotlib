"""
Plot an image map of bedrock surface elevation.
"""

import iceplotlib.plot as iplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
iplt.axes(projection='mapaxes')
iplt.icemargin(nc, thkth=1.0)

# show
nc.close()
iplt.show()
