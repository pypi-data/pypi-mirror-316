






'''
	from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.search_one import search_one_trend
	search_one_trend ({
		"filter": {
			"nature.identity.FDC ID": ""
		}
	})
'''



#/
#
from prosthetic._essence import retrieve_essence
from prosthetic.adventures.monetary.DB_prosthetic_trends.connect import connect_to_prosthetic_inventory
#
#
import ships.modules.exceptions.parse as parse_exception
#
#
import pymongo
#
#
import time
#
#\



def search_one_trend (packet):
	filter = packet ["filter"]
	trend = ""

	print ("filter:", filter)

	try:
		[ driver, DB_prosthetic_trends ] = connect_to_prosthetic_inventory ()
		collection_vernacular = DB_prosthetic_trends ["collection_vernacular"]
	except Exception as E:
		print ("collection_vernacular connect exception:", E)
		
	
	try:	
		essence = retrieve_essence ()
		trend = collection_vernacular.find_one (filter)
		
	except Exception as E:
		print ("collection_vernacular find_one exception:", parse_exception.now (E))
		
	try:
		driver.close ()
	except Exception as E:
		print (parse_exception.now (E))
		print ("collection disconnect exception:", parse_exception.now (E))	
		
		
	return trend;








