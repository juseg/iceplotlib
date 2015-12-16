"""
Plot surface velocity vectors.
"""

import iceplotlib.plot as iplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
nc.quiver('velsurf')
nc.icemargin()

# show
nc.close()
iplt.show()
