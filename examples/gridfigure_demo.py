"""
Draw multi-panel figure.
"""

import iceplotlib.plot as iplt

# initialize figure
fig = iplt.gridfigure((30., 60.), (2, 3), cbar_mode='single')

# load data
nc = iplt.load('pism_plot_sample.nc')

# plot
for ax in fig.grid:
    ax.icemap(nc, thkth=1.0)

# add colorbar
cb = fig.colorbar(im, ax.cax)
cb.set_label('ice surface velocity (m/s)')

# show
iplt.show()
