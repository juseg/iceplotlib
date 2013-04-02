"""pismplot.cm

Provide custom colormaps.
"""

from matplotlib.colors import LinearSegmentedColormap

# Topography colormaps

_sea_topo_bounds = [1-z/6000. for z in
  [6000, 5000, 4000, 3000, 2000, 1000, 500, 200, 100, 0]]

_sea_topo_clist = [
 '#71abd8', '#79b2de', '#84b9e3', '#8dc1ea', '#96c9f0', '#a1d2f7',
 '#acdbfb', '#b9e3ff', '#c6ecff', '#d8f2fe']

sea_topo = LinearSegmentedColormap.from_list(
  'sea_topo', zip(_sea_topo_bounds, _sea_topo_clist))

_land_topo_bounds= [z/6000. for z in
  [    0,    1,  100,  250,  500,  750, 1000, 1250, 1500, 1750,
    2000, 2250, 2500, 2750, 3000, 3500, 4000, 4500, 5000, 6000]]

_land_topo_clist = [
 '#d8f2fe', '#94bf8b', '#acd0a5', '#a8c68f', '#bdcc96', '#d1d7ab',
 '#e1e4b5', '#efebc0', '#e8e1b6', '#ded6a3', '#d3ca9d', '#cab982',
 '#c3a76b', '#b9985a', '#aa8753', '#ac9a7c', '#baae9a', '#cac3b8',
 '#e0ded8', '#f5f4f2']

land_topo = LinearSegmentedColormap.from_list(
  'land_topo', zip(_land_topo_bounds, _land_topo_clist))

_topo_bounds = [z/2 for z in _sea_topo_bounds[:-1]] + \
  [(z+1)/2 for z in _land_topo_bounds]

_topo_clist = _sea_topo_clist[:-1] + _land_topo_clist

topo = LinearSegmentedColormap.from_list(
  'topo', zip(_topo_bounds, _topo_clist))

# Other colormaps

_velocity_clist = [
  '#ffffff', '#00ffff', '#ffff00', '#ff0000', '#000000']

velocity = LinearSegmentedColormap.from_list(
  'velocity', _velocity_clist)

