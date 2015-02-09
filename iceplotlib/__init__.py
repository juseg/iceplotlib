""":mod:`iceplotlib`

A plotting library for `PISM`_ using `matplotlib`_ and `netcdf4-python`_.

.. links

.. _netcdf4-python: http://unidata.github.io/netcdf4-python/
.. _matplotlib: http://matplotlib.org
.. _PISM: http://www.pism-docs.org
"""

from matplotlib import pyplot as plt

plt.rc('font', size=6)
plt.rc('image', interpolation='nearest', origin='lower')
plt.rc('savefig', dpi=254)
