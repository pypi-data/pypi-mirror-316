



''''
	from prosthetic.treasures.pass_to_trends import pass_treasure_to_trends
	[ status, result_notes ] = pass_treasure_to_trends ({
		"domain": "waste.1",
		"similar": []
	});
"'''

''''
	status:
		victory
		defeat
"'''



#/
#
import shutil
import io
import os
#
#
import ships.paths.directory.check_equality as check_equality
#
#
from prosthetic.frontiers.treasures._quests.itemize import itemize_treasures
from prosthetic.frontiers.treasures.check.domain_fiber import check_domain_fiber
#
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.insert import insert_document
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.search_one import search_one_trend
#
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_novels.document.insert import insert_novel
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_novels.document.retrieve import retrieve_novel
#
from prosthetic._essence import retrieve_essence
#
from prosthetic.mixes.zipping.make_zip import make_zip
from prosthetic.mixes.zipping.make_dir import make_dir
#
#\

		

#
#	moves:
#		1. zip the treasure with "ships"
#		2. save to GridFS
#		3. retrieve from GridFS
#		4. check equality
#		
#
def pass_treasure_to_trends (packet):

	print ("pass_treasure_to_trends");

	try:
		domain = packet ["domain"]
		similar = []
		if ("similar" in packet):
			similar = packet ["similar"]

		essence = retrieve_essence ()
		the_mix_directory = essence ["the_mix_directory"]
		treasures_path = essence ["treasures"] ["path"]
		ephemeral_path = essence ["ephemeral"] ["path"]

		domain_directory = str (os.path.normpath (os.path.join (treasures_path, domain)));
		domain_zip_path_without_extension = str (os.path.normpath (os.path.join (ephemeral_path, domain + "-zip")));
		domain_directory_extracted = str (os.path.normpath (os.path.join (ephemeral_path, domain + "-extracted")));

		
		#
		#
		#	Make sure there's only 1 trend domain in the database.
		#
		#
		trend = search_one_trend ({
			"filter": {
				"domain": domain
			}
		});
		if (trend != None):
			return [ "defeat", "That domain already exists" ]
		


		#treasures = itemize_treasures ()
		print ("pass treasure", domain_directory);	
		
		
		
		#
		#	* zip the directory
		#	* insert the zipped directory
		#
		zip_data = make_zip ({ 
			"directory_path": domain_directory,
			"zip_path_without_extension": domain_zip_path_without_extension
		});
		insertion = insert_novel ({ "zip_buffer": zip_data });
		novella_id = insertion ["_id"]
		print ("novella_id:", novella_id);
		
		#
		#	* retrieve the zipped directory
		#	* create directory from the zipped directory
		#
		retrieved = retrieve_novel ({
			"_id": novella_id
		});
		zip_buffer_2 = retrieved ["zip_buffer"]
		make_dir (zip_buffer_2, domain_directory_extracted);

		
		#
		#	* 	make sure that the unzipped directory
		#		is equivalent to the treasure directory.
		#
		report = check_equality.start (domain_directory, domain_directory_extracted)	
		assert (
			report ==
			{'1': {}, '2': {}}
		)
		print ("The equality vow for the [ directory -> zip -> GridFS -> directory ] passed.")

		
		#
		#	*	insert trend document
		#
		#
		try:
			insert_document ({
				"document": {
					"domain": domain,
					"novella": str (novella_id),
					"similar": similar
				}
			});
		except Exception as E:
			print ("trend insertion exception:", E);
			return [ "defeat", "The trend could not be added." ]
		
		#
		#	* Remove the emperemal directories
		#	
		#
		os.remove (domain_zip_path_without_extension + ".zip")
		shutil.rmtree (domain_directory_extracted)
		
		#
		#	* 	Remove the treasure directory.
		#		The equality check should ensure that the zip file was inserted.
		#
		shutil.rmtree (domain_directory)
		
	except Exception as E:
		print ("treasure to trends exception:", E);
		return [ "defeat", "An imperfection occurred whilest passing treasure to trends." ]
	
	
	return [ "victory", "" ]