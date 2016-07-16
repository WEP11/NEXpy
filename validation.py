######################################
#                                    #
#		     validation.py           #
#                                    #
######################################
#
# CONTAINS LISTS AND FUNCTIONS NECESSARY FOR
# OBTAINING NEXRAD DATA
#
# Component of NEXpy
#


# Lists of valid radar sites
NWS_SITES = ['ABR','ENX','ABX','AMA','AHG','GUA','FFC','BBX','ABC','BLX','BGM','ACG','BMX','BIS',
'FCX','CBX','BOX','BRO','BUF','CXX','FDX','CBW','ICX','GRK','CLX','RLX','CYS','LOT','ILN',
'CLE','CAE','GWX','CRP','FTG','DMX','DTX','DDC','DOX','DLH','DYX','EYX','EPZ','LRX','BHX',
'VWX','APD','FSX','SRX','FDR','HPX','POE','EOX','FWS','APX','GGW','GLD','MVX','GJX','GRR',
'TFX','GRB','GSP','UEX','HDX','HGX','HTX','IND','JKL','DGX','JAX','HKM','EAX','BYX','AKC',
'MRX','ARX','LCH','LGX','ESX','DFX','ILX','LZK','VTX','LVX','LBB','MQT','MXX','MAX','MLB',
'NQA','AMX','AIH','MAF','MKX','MPX','MBX','MSX','MOB','HMO','TYX','VAX','MHX','OHX','LIX',
'OKX','AEC','LNX','IWX','EVX','TLX','OAX','PAH','PDT','DIX','IWA','PBZ','SFX','GYX','RTX',
'PUX','DVN','RAX','UDX','RGX','RIW','JGX','DAX','MTX','SJT','EWX','NKX','MUX','HNX','JUA',
'SOX','ATX','SHV','FSD','HKI','HWA','OTX','SGF','LSX','CCX','LWX','TLH','TBW','TWX','EMX',
'INX','VNX','VBX','AKQ','ICT','LTX','YUX']

FAA_SITES = ['ADW','ATL','BNA','BOS','BWI','CLT','CMH','CVG','DAL','DAY','DCA','DEN','DFW',
'DTW','EWR','FLL','HOU','IAD','IAH','ICH','ICT','IDS','JFK','JUA','LAS','LSX','LVE','MCI','MCO',
'MDW','MEM','MIA','MKE','MSP','MSY','OKC','ORD','PBI','PHL','PHX','PIT','RDU','SDF','SJU','SLC',
'STL','TBW','TPA','TUL']

# Lists of valid products
# BaseReflectivity
# BaseReflectivityDR

PRODUCTS_88D = {"N0Q":"BaseReflectivityDR",
"N1Q":"BaseReflectivityDR",
"N1Q":"BaseReflectivityDR",
"N2Q":"BaseReflectivityDR",
"N3Q":"BaseReflectivityDR",
"N0U":"BaseVelocityDV",
"N1U":"BaseVelocityDV",
"N2U":"BaseVelocityDV",
"N3U":"BaseVelocityDV",
"DHR":"DigitalHybridReflectivity",
"NCR":"BaseReflectivityComp",
"NCZ":"BaseReflectivityComp",
"NET":"EchoTops",
"EET":"EnhancedEchoTops",
"N0S":"StormRelativeVelocity",
"N1S":"StormRelativeVelocity",
"N2S":"StormRelativeVelocity",
"N3S":"StormRelativeVelocity",
"VIL":"VerticallyIntegratedLiquid",
"N1P":"1HourRainfall",
"N3P":"3HourRainfall",
"NTP":"StormTotalRainfall",
"DSP":"DigitalStormTotalPrecipitation",
"N0X":"DigitalDifferentialReflectivity",
"N1X":"DigitalDifferentialReflectivity",
"N2X":"DigitalDifferentialReflectivity",
"N3X":"DigitalDifferentialReflectivity",
"N0C":"CorrelationCoefficient",
"N1C":"CorrelationCoefficient",
"N2C":"CorrelationCoefficient",
"N3C":"CorrelationCoefficient"}

FAA_PRODUCTS = {"TR0":"BaseReflectivity","TR1":"BaseReflectivity","TR2":"BaseReflectivity","TR3":"BaseReflectivity",
"TV0":"BaseVelocity","TV1":"BaseVelocity","TV2":"BaseVelocity","TV3":"BaseVelocity",
"DHR":"DigitalHybridReflectivity","NCR":"BaseReflectivityComp","NET":"EchoTops","NVL":"VerticalIntegratedLiquid",
"DSP":"StormTotalPrecipitation"}

# FUNCTIONS -----------------------------------------------------------------------------

# Checks whether a site is a WSR-88D or TDWR...
def checkRadarType(site):
	
	for i in NWS_SITES:
		if site == i:
			return '88D'

	for i in FAA_SITES:
		if site == i:
			return 'TDWR'

	return 'UNKNOWN SITE'

# Find the product variable name...
def checkProduct(product):

	for i in PRODUCTS_88D:
		if i==product:
			return PRODUCTS_88D[i]

	for i in FAA_PRODUCTS:
		if i==product:
			return FAA_PRODUCTS[i]

	return 'UNAVAILABLE PRODUCT'

def checkColorTable(product):
	
	if (product == 'N0Q' or product == 'N1Q' or product == 'N2Q' or product == 'N3Q' or
product == 'TR0' or product == 'TR1' or product == 'TR2' or product == 'TR3' or product == 'DHR' or product == 'NCR'):
		return 'NWSReflectivity'

	elif (product == 'N0U' or product == 'N1U' or product == 'N2U' or product == 'N3U' or
product == 'TV0' or product == 'TV1' or product == 'TV2' or product == 'TV3'):
		return 'NWSVelocity'

