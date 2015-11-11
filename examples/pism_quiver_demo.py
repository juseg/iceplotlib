"""
Plot surface velocity vectors.
"""

import iceplotlib.plot as iplt

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
nc.quiver('velsurf', thkth=1.0)
nc.icemargin(thkth=1.0)

# show
nc.close()
iplt.show()
