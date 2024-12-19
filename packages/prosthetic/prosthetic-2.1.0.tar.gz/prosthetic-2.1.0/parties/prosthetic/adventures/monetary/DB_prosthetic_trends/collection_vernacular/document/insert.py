


'''
	from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.insert import insert_document
	insert_document ({
		"document": {
			"domain": ""
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


'''
	FDC_ID = "",
	affiliates = [],
	goodness_certifications = []
'''
def insert_document (packet):
	document = packet ["document"]
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
	#	Insert and ensure that inserted correctly.
	#
	#		except pymongo.errors.DuplicateKeyError:
	#
	inserted = collection_vernacular.insert_one (document)
	inserted_document = collection_vernacular.find_one ({"_id": inserted.inserted_id })
	print ("inserted:", inserted_document)
	
	
	#
	#
	#	Close the connection
	#
	#
	driver.close ()
		









