#######################################################
#                                                     #
#         PYTHON NEXRAD PLOT GENERATION               #
#                                                     #
#              Level-3, Single Site                   #
#                                                     #
#  UNC CHARLOTTE DEVELOPER: Warren Pettee (@wpettee)  #
#                                                     #
#                   V 1.0.0                           #
#                                                     #
#######################################################
#
# CHANGELOG:
# Authored - Aug-2015 (Warren Pettee)
#
#######################################################
#
#

import argparse

from siphon.radarserver import RadarServer
from datetime import datetime
from siphon.cdmr import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy
from metpy.plots import ctables

#from mpl_toolkits.basemap import Basemap, shiftgrid

#------------------------------------------------------
# Command Line Functions:
parser = argparse.ArgumentParser(description='NEXRAD/TDWR Site Information')

parser.add_argument('site',
                    help='3-Letter Site Identifier (WSR-88D or TDWR)')
parser.add_argument('product',
                    help='3-Letter Product Identifier (See RPCCDS list at NWS)\nExample:Reflectivity(N0R or TR0)\nVelocity(N0V or TV0)')

args = parser.parse_args()

# WHAT TIME IS IT? ------------------------------------
year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
hour = datetime.today().hour
minute = datetime.today().minute

## TODO: Find previous frame times. timedelta?


# ACQUIRE DATA ----------------------------------------

rs = RadarServer('http://thredds.ucar.edu/thredds/radarServer/terminal/level3/IDD/')

query = rs.query()
query.stations(args.site).time(datetime(year, month, day, hour, minute)).variables(args.product)

rs.validate_query(query)

catalog = rs.get_catalog(query)

catalog.datasets

ds = list(catalog.datasets.values())[0]
ds.access_urls

# READ DATA ------------------------------------------

data = Dataset(ds.access_urls['CdmRemote'])
#print data.variables ### DEBUG

rng = data.variables['gate'][:]
az = data.variables['azimuth'][:]
ref = data.variables['BaseReflectivity'][:]

x = rng * np.sin(np.deg2rad(az))[:, None]
y = rng * np.cos(np.deg2rad(az))[:, None]
ref = np.ma.array(ref, mask=np.isnan(ref))

# BEGIN PLOTTING --------------------------------------------------

# Create projection centered on the radar. This allows us to use x
# and y relative to the radar.
proj = cartopy.crs.LambertConformal(central_longitude=data.RadarLongitude,
                                    central_latitude=data.RadarLatitude)

# New figure with specified projection
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1, projection=proj)

# Grab state borders
#state_borders = cartopy.feature.NaturalEarthFeature(
#    category='cultural', name='admin_1_states_provinces_lines',
#    scale='50m', facecolor='none')
#ax.add_feature(state_borders, edgecolor='black', linewidth=2, zorder=2)

# Counties
counties = cartopy.io.shapereader.Reader('data/counties')
ax.add_geometries(counties.geometries(), cartopy.crs.PlateCarree(),
                  facecolor='#C2A385', edgecolor='grey', zorder=1)

# Interstates
interstate = cartopy.io.shapereader.Reader('data/interstates')
ax.add_geometries(interstate.geometries(), cartopy.crs.PlateCarree(),
                  facecolor='none', edgecolor='#B20000', zorder=1)

# Hydrography
#hydro = cartopy.io.shapereader.Reader('data/hydro')
#ax.add_geometries(hydro.geometries(), cartopy.crs.PlateCarree(),
#                 facecolor='none', edgecolor='#ADD6FF', zorder=1)

# Set limits in lat/lon space
# LonW, LonE, LatN, LatS
#ax.set_extent([-81.8, -80, 36, 34.5])

norm, cmap = ctables.registry.get_with_steps('NWSReflectivity', 5, 5)
ax.pcolormesh(x, y, ref, cmap=cmap, norm=norm, zorder=2)

title_line1 = str(args.site)
plt.title(title_line1,color='k',fontsize=18,fontweight='bold',style='italic')
plt.savefig('/home/warren/Desktop/nexpy/TCLTref.png',format='png')

plt.show()
