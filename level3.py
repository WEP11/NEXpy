#######################################################
#                                                     #
#         PYTHON NEXRAD PLOT GENERATION               #
#                                                     #
#              Level-3, Single Site                   #
#                                                     #
#            Warren Pettee (@wpettee)                 #
#                                                     #
#                                                     #
#######################################################


import argparse
import sys
import time
from datetime import datetime, timedelta

import threading
from threading import Thread

from siphon.radarserver import RadarServer
from siphon.cdmr import Dataset

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation

mpl.rcParams['toolbar'] = 'None'

import cartopy

from metpy.plots import ctables

import validation
#------------------------------------------------------

def update(frame):
	global SITE
	global PRODUCT
	
	print("Building Frame:",frame)
	#What is the age of this frame?
	frameIndex = frame % 9
	frameAge = frameIndex * 10 # minutes old

	# WHAT TIME WILL THE FRAME BE??
	date = datetime.utcnow() - timedelta(minutes=frameAge)
	year = date.year
	month = date.month
	day = date.day
	hour = date.hour
	minute = date.minute


	# What type of radar site is this?..
	
	siteType = validation.checkRadarType(SITE)
	ncfVar = validation.checkProduct(PRODUCT)
	colorTable = validation.checkColorTable(PRODUCT)

	if siteType=='88D':
		rs = RadarServer('http://thredds.ucar.edu/thredds/radarServer/nexrad/level3/IDD/')
	elif siteType=='TDWR':
		rs = RadarServer('http://thredds.ucar.edu/thredds/radarServer/terminal/level3/IDD/')
	else:
		print('INVALID SITE IDENTIFIER')
		sys.exit()


	# ACQUIRE DATA ----------------------------------------

	query = rs.query()
	query.stations(args.site).time(datetime(year,month,day,hour,minute)).variables(args.product)

	rs.validate_query(query)

	catalog = rs.get_catalog(query)

	catalog.datasets

	ds = list(catalog.datasets.values())[0]
	ds.access_urls

	# READ DATA ------------------------------------------
	data = Dataset(ds.access_urls['CdmRemote'])

	rng = data.variables['gate'][:]
	az = data.variables['azimuth'][:]
	ref = data.variables[ncfVar][:]

	x = (rng * np.sin(np.deg2rad(az))[:, None])
	y = (rng * np.cos(np.deg2rad(az))[:, None])
	ref = np.ma.array(ref, mask=np.isnan(ref))
	plot = ax.pcolormesh(x, y, ref, cmap=cmap, norm=norm, zorder=2)
	title_line1 = '%s %s - %i:%i' % (args.site,args.product,hour,minute)
	plt.title(title_line1,color='k',fontsize=18,fontweight='bold',style='italic')

	return plot

# Command Line Functions:
parser = argparse.ArgumentParser(description='NEXRAD/TDWR Site Information')

parser.add_argument('site',
                    help='3-Letter Site Identifier (WSR-88D or TDWR)')
parser.add_argument('product',
                    help='3-Letter Product Identifier (See RPCCDS list at NWS)\nExample:Reflectivity(N0R or TR0)\nVelocity(N0V or TV0)')
parser.add_argument('animate',
                    help='Build animated image? "true" or "false"')

args = parser.parse_args()

SITE=args.site
PRODUCT=args.product

# WHAT TIME IS IT? ------------------------------------
date = datetime.utcnow()
year = datetime.utcnow().year
month = datetime.utcnow().month
day = datetime.utcnow().day
hour = datetime.utcnow().hour
minute = datetime.utcnow().minute


# What type of radar site is this?..
	
siteType = validation.checkRadarType(args.site)
ncfVar = validation.checkProduct(args.product)
colorTable = validation.checkColorTable(args.product)

if siteType=='88D':
	rs = RadarServer('http://thredds.ucar.edu/thredds/radarServer/nexrad/level3/IDD/')
elif siteType=='TDWR':
	rs = RadarServer('http://thredds.ucar.edu/thredds/radarServer/terminal/level3/IDD/')
else:
	print('INVALID SITE IDENTIFIER')
	sys.exit()


# ACQUIRE DATA ----------------------------------------

query = rs.query()
query.stations(args.site).time(datetime(year,month,day,hour,minute)).variables(args.product)

rs.validate_query(query)

catalog = rs.get_catalog(query)

catalog.datasets

ds = list(catalog.datasets.values())[0]
ds.access_urls

# READ DATA ------------------------------------------
print("--- AQUIRING DATA ---")
data = Dataset(ds.access_urls['CdmRemote'])
print("Aquisition Complete!!")
#print (data.variables) ### DEBUG

rng = data.variables['gate'][:]
az = data.variables['azimuth'][:]
ref = data.variables[ncfVar][:]

x = (rng * np.sin(np.deg2rad(az))[:, None])
y = (rng * np.cos(np.deg2rad(az))[:, None])
ref = np.ma.array(ref, mask=np.isnan(ref))

# BEGIN PLOTTING --------------------------------------------------
### TODO: Losing loading time in county rendering.. fix me

# Create projection centered on the radar. This allows us to use x
# and y relative to the radar.
proj = cartopy.crs.LambertConformal(central_longitude=data.RadarLongitude,
                                    central_latitude=data.RadarLatitude)

# New figure with specified projection
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1, projection=proj)

print("Loading geography overlays...")
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

print("Building Figure...")
norm, cmap = ctables.registry.get_with_steps(colorTable, 5, 5)
plot = ax.pcolormesh(x, y, ref, cmap=cmap, norm=norm, zorder=2)
#ax.contourf(x, y, ref, cmap=cmap, norm=norm, zorder=2)
title_line1 = '%s %s - %i:%i' % (args.site,args.product,hour,minute)
plt.title(title_line1,color='k',fontsize=18,fontweight='bold',style='italic')

if args.animate == 'true':
	animation = animation.FuncAnimation(fig, update, interval=15, blit=False, frames=10)
	animation.save('nexpy.gif', writer='imagemagick', fps=15, dpi=40)

plt.show()

