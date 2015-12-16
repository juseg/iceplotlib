"""
Plot surface velocity streamlines.
"""

import iceplotlib.plot as iplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
nc.streamplot('velsurf')
nc.icemargin()

# show
nc.close()
iplt.show()
