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
