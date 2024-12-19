
''''
	from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_novels.document.insert import insert_novel
	insertion = insert_novel ({
		"zip_buffer": ""
	});
	
	novella_id = insertion ["_id"]
"'''


from pymongo import MongoClient
from gridfs import GridFS

from prosthetic.adventures.monetary.DB_prosthetic_trends.connect import connect_to_prosthetic_inventory


def insert_novel (packet):
	zip_buffer = packet ["zip_buffer"]
	name = "name-1"
	metadata = {}

	[ driver, prosthetic_inventory_DB ] = connect_to_prosthetic_inventory ()
	collection_novels = prosthetic_inventory_DB ["collection_novels"]
	fs = GridFS (prosthetic_inventory_DB, collection = "novellas")

	id = fs.put (
		zip_buffer, 
		filename = name + '.zip', 
		metadata = metadata
	)
	
	print ("id:", id);
	
	driver.close ()
	
	return {
		"_id": id
	}