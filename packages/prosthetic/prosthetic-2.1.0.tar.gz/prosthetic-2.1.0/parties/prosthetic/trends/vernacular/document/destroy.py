
'''
	from prosthetic.trends.vernacular.document.destroy import destroy_vernacular_document
	destroy_vernacular_document ({
		"sieve": {
			"domain": ""
		}
	})
'''


#/
#
import time
#
#
import pymongo
#
#
import ships.modules.exceptions.parse as parse_exception
#
#
from prosthetic._essence import retrieve_essence
from prosthetic.adventures.monetary.DB_prosthetic_trends.connect import connect_to_prosthetic_inventory
#
#\



def destroy_vernacular_document (packet):
	sieve = packet ["sieve"]
	essence = retrieve_essence ()

	#
	#
	#	Connect to mongo
	#
	#
	[ driver, DB_prosthetic_trends ] = connect_to_prosthetic_inventory ()
	collection_vernacular = DB_prosthetic_trends ["collection_vernacular"]

	#
	#
	#	Deletion
	#
	#
	deletion = collection_vernacular.delete_one (sieve);
	print ("vernacular deletion:", deletion);
	
	#
	#
	#	Close the connection
	#
	#
	driver.close ()
		