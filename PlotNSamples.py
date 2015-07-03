
"""
    Script to plot the number of observations/samples available
    within a 32-day window of the MELODIES BRDF product
"""

from os.path import basename as bn

import matplotlib as mpl
# Use a non-interactive backend
mpl.use('Agg')

from pylab import *
from osgeo import gdal as gdal
import numpy as np

__author__ = "Gerardo Lopez-Saldana (UREAD)"
__copyright__ = "(c) 2015"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "G Lopez-Saldana"
__email__ = "G.LopezSaldana@reading.ac.uk"
__status__ = "Development"

from os.path import basename as bn

import matplotlib as mpl
# Use a non-interactive backend
mpl.use('Agg')

from pylab import *
from osgeo import gdal as gdal
import numpy as np

# File with data to plot
file = sys.argv[1]
# Band to plot - e.g. 2007161.NSamples.vrt
band = int ( sys.argv[2] )

dataset = gdal.Open( file )
DoY = bn( file )[0:7]

NSamples = dataset.GetRasterBand( band ).ReadAsArray()
# When there are 1 - 6 samples the BRDF model inversion
# is not performed, mask that range then.
NSamples = np.ma.masked_inside( NSamples, 1., 6. )

# Modify the standard Summer colorbar
# 'bad values' are in grey.
cmap = mpl.cm.summer
cmap._init()
# 'bad/masked values' are in grey
cmap.set_bad('grey', 1. )
# first value, in this case 0, is white (RGB 1,1,1 alpha channel 1)
cmap._lut[0,:] = [ 1,1,1,1 ]

MaxNumberOfSamples = 50
SamplesForBRDF = 6

from IPython import embed
ipshell = embed()
# Set to grey RGB (128,128,128) where there are 1 - 6 samples
UpperGreyLimit = ( cmap._lut.shape[0] / ( MaxNumberOfSamples + 1 ) ) * SamplesForBRDF
cmap._lut[1:UpperGreyLimit ,:] = [ 128,128,128,1 ]

imshow( NSamples, cmap = cmap, vmin = 0, vmax = MaxNumberOfSamples)
colorbar()
plt.axis('off')

# Title
plt.title( str( DoY ) )
# Save fig to a png file
savefig('NSamples.' + DoY + '.png', 
        dpi = 300, bbox_inches = 'tight', 
        pad_inches = 0., transparent = False )
