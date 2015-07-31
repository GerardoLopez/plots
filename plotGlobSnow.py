from pylab import *
from mpl_toolkits.basemap import Basemap

from netCDF4 import Dataset
import numpy as np

GlobSnow_fname = 'GlobSnow_SWE_L3A_20101201_v2.0.nc'
SWE_d = Dataset( GlobSnow_fname, mode='r')

# Read variables
# Do a gdalinfo to find out the content of the NetCDF file
lons = SWE_d.variables['lon'][:]
#lons = np.rot90(lons)
#lons = np.rot90(lons)

lats = SWE_d.variables['lat'][:]
SWE = SWE_d.variables['SWE'][:]
# Mask array
SWE = np.ma.masked_where( SWE < 0, SWE )
from IPython import embed
ipshell = embed()

SWE_units = SWE_d.variables['SWE'].units

# Close dataset
SWE_d.close()

# Create basemap instance
# Polar Lambert Azimuthal Projection
m = Basemap(projection='nplaea', boundinglat = 35, lon_0 = 0, resolution='l')
# Transform to map coordinates
# in this case is specifically neede cause the lats array is rotated
# check it ploting lats and lons array, e.g. imshow(lats)
x, y = m( lons, lats )

# Modify the standard Blues colorbar
# 'bad values' are in grey.
cmap = mpl.cm.Blues
cmap._init()
# 'bad/masked values' are in grey
cmap.set_bad('grey', 1. )
# first value, in this case 0, is white (RGB 1,1,1 alpha channel 1)
cmap._lut[0,:] = [ 1,1,1,1 ]

# Plot Data
SWE_plot = m.pcolor(x, y, SWE, zorder = 0, cmap = cmap )

# Overlay coastlines and country oundaries
m.drawcoastlines( zorder = 1 )
m.drawcountries( zorder = 1 )

# Parallels and meridians
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))

# Add Colorbar
cbar = m.colorbar( SWE_plot, location='bottom', pad="10%")
cbar.set_label( SWE_units)

# Add Title - thankfully not SMA...
title('SWE')

show()
