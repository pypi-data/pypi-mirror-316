
''''
	perhaps: _id should be string
"'''

''''
	from .novellas.document.destroy import destroy_novella
	destroy_novella ({ "_id": "" });
"'''


from pymongo import MongoClient
from gridfs import GridFS
from gridfs.errors import NoFile

from prosthetic.adventures.monetary.DB_prosthetic_trends.connect import connect_to_prosthetic_inventory

def destroy_novella (packet):
	_id = packet ["_id"]

	[ driver, prosthetic_inventory_DB ] = connect_to_prosthetic_inventory ()
	
	GFS_Driver = GridFS (prosthetic_inventory_DB, collection = "novellas")
	
	deletion = GFS_Driver.delete (_id)
	print ("deletion:", deletion);
	
	has_novella = "no"
	try:
		novella_document = GFS_Driver.get (_id)
		print ("novella document:", novella_document)
	except NoFile:
		has_novella = "yes"
	
	if (has_novella == "no"):
		raise Exception ("The novella wasn't deleted.")
	
	driver.close ()
