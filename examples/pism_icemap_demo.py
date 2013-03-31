"""
Draws the module's canonical icemap and add a colorbar.
"""

from matplotlib import pyplot as plt
from netCDF4 import Dataset
from iceplot import plot as pplt

# load data
nc = Dataset('extra.nc')

# plot
im = pplt.icemap(nc, t=-1)

# add colorbar
cb = plt.colorbar(im)
cb.set_label('ice surface velocity (m/yr)')

# save
plt.show()

