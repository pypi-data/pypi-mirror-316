


'''
	import prosthetic.modules.moves.trends.extract_to_temp as extract_to_temp
	extract_to_temp.extract (_id, original_directory_path)
'''

#----
#
from prosthetic._essence import retrieve_essence
#
#
import ships.paths.directory.check_equality as check_equality
#
#
from bson import ObjectId	
import io
import zipfile
import tempfile
from pymongo import MongoClient
#
#---


def extract (_id, original_directory_path = ""):
	print ()
	print ("extracting to temp")

	GridFS = essence.link_FS ()
	
	zip_document = GridFS.get (ObjectId (_id))
	print ('	zip_document:', zip_document)
	
	zip_data = io.BytesIO (zip_document.read ())
	print ('	zip_data:', zip_data)

	with tempfile.TemporaryDirectory () as temp_dir:
		#
		#	Extract the ZIP file to the temporary directory
		#
		with zipfile.ZipFile (zip_data, 'r') as zip_ref:
			zip_ref.extractall (temp_dir)
		
			print("ZIP file extracted to temporary directory:", temp_dir)
		
			report = check_equality.start (
				temp_dir,
				original_directory_path
			)	
			assert (
				report ==
				{'1': {}, '2': {}}
			)
			
			print ("zip equality check passed")
	

	print ()
