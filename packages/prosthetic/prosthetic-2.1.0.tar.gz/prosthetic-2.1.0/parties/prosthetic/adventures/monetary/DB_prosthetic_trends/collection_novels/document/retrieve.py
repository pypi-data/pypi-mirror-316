


''''
	from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_novels.document.retrieve import retrieve_novel
	retrieved = retrieve_novel ({
		"_id": ""
	});
	
	zip_buffer = retrieved ["zip_buffer"]
"'''


from pymongo import MongoClient
from gridfs import GridFS

from prosthetic.adventures.monetary.DB_prosthetic_trends.connect import connect_to_prosthetic_inventory


def retrieve_novel (packet):
	_id = packet ["_id"]

	[ driver, prosthetic_inventory_DB ] = connect_to_prosthetic_inventory ()
	fs = GridFS (prosthetic_inventory_DB, collection = "novellas")

	print ("_id:", _id)

	file = fs.get (_id)
	zip_buffer = file.read ()
	
	driver.close ()
	
	return {
		"zip_buffer": zip_buffer
	}