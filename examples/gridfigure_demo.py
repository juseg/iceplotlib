"""
Draw multi-panel figure.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from iceplot import plot as iplt

# initialize figure
fig = iplt.gridfigure((30., 60.), (2, 3), cbar_mode='single')

# load data
nc = Dataset('pism_plot_sample.nc')

# plot
for ax in fig.grid:
  mplt.axes(ax)
  im = iplt.icemap(nc, axes=ax)

# add colorbar
cb = fig.colorbar(im, ax.cax)
cb.set_label('ice surface velocity (m/s)')

# show
mplt.show()
