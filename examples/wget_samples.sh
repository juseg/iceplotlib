#!/bin/bash

# Download plot samples used in the docs.
#
# * `pism_anim_sample.nc` contains contains modelled surface and basal
#   topography, ice thickness and surface velocities showing the growth
#   and decay of the Cordilleran ice sheet over 20 ka.
# * `pism_plot_sample.nc` contains only one time slice located in the
#   middle of that interval but has more output variables from PISM.

wget https://dl.dropbox.com/s/ziah7cahlshuxgh/pism_plot_sample.nc
wget https://dl.dropbox.com/s/6e3sga0bmabd275/pism_anim_sample.nc
