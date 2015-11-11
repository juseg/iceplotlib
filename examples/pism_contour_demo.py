"""
Plot an image map of bedrock surface elevation.
"""

import iceplotlib.plot as iplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
nc.contour('usurf', thkth=1.0, colors='black')
nc.icemargin(thkth=1.0)

# show
nc.close()
iplt.show()
