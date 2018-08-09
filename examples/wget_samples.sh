#!/bin/bash

# Download plot samples used in the docs.
#
# * `pism_anim_sample.nc` contains contains modelled surface and basal
#   topography, ice thickness and surface velocities showing the growth
#   and decay of the Cordilleran ice sheet over 20 ka.
# * `pism_plot_sample.nc` contains only one time slice located in the
#   middle of that interval but has more output variables from PISM.

wget https://polybox.ethz.ch/index.php/s/VK61I775Lx4VWka/download -O pism_plot_sample.nc
wget https://polybox.ethz.ch/index.php/s/NK3JYQLr8Kb2RLB/download -O pism_anim_sample.nc
