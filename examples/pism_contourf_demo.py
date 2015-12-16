"""
Plot an image map of bedrock surface elevation.
"""

import iceplotlib.plot as iplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
nc.contourf('topg')

# show
nc.close()
iplt.show()
