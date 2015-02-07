"""
Animation demo.
"""

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplot import animation as iani

# load data
nc = Dataset('pism_anim_sample.nc')

# animate
ani = iani.iceanim(nc)

# show
plt.show()

# to save the animation:
#ani.save('iceanim.mp4')
