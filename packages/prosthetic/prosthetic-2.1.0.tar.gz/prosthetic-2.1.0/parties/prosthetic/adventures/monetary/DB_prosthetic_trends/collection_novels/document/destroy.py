
''''
	from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_novels.document.destroy import destroy_novel
	destroy_novella ({
		"_id": ""
	});
"'''


from pymongo import MongoClient
from gridfs import GridFS

from prosthetic.adventures.monetary.DB_prosthetic_trends.connect import connect_to_prosthetic_inventory

def destroy_novella (packet):
	_id = packet ["_id"]

	[ driver, prosthetic_inventory_DB ] = connect_to_prosthetic_inventory ()
	
	GFS_Driver = GridFS (prosthetic_inventory_DB, collection = "novellas")
	GFS_Driver.delete (_id)
	
	driver.close ()
