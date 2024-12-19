

''''
	from prosthetic.trends.pass_trend_to_treasures import pass_trend_to_treasures
	[ status, result_notes ] = pass_trend_to_treasures ({
		"domain": "waste.1"
	});
"'''

''''
	status:
		victory
		defeat
"'''

#/
#
import ast
from pprint import pprint
import os
#
#
import click
#
#
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.insert import insert_document
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.search import search_trends_vernacular
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.count import count_treasures
#
from prosthetic.frontiers.trends.quests.saves._clique import saves_clique
#
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_novels.document.retrieve import retrieve_novel
#
#\

from prosthetic.mixes.zipping.make_dir import make_dir
from prosthetic.trends.vernacular.document.destroy import destroy_vernacular_document
from prosthetic._essence import retrieve_essence
#
from .novellas.document.destroy import destroy_novella
#
#


from bson import ObjectId
from pathlib import Path

def pass_trend_to_treasures (packet):
	#/
	#
	domain = packet [ "domain" ]
	#
	#
	essence = retrieve_essence ()
	treasures_path = essence ["treasures"] ["path"]
	domain_directory = str (os.path.normpath (os.path.join (treasures_path, domain)));
	#
	#\

	treasures = search_trends_vernacular ({
		"filter": {
			"domain": domain
		}
	});
	
	assert (len (treasures) == 1)
	treasure = treasures [0]
	pprint (treasure, indent = 4)
	
	if ("novella" in treasure):
		print ("novella found");
		
		retrieved = retrieve_novel ({
			"_id": ObjectId (treasure ["novella"])
		});
		zip_buffer_2 = retrieved ["zip_buffer"]

		if (os.path.exists (domain_directory)):
			return [ "defeat", "A directory with that domain name already exists" ]

		#
		#
		#	Make the treasure from the zip buffer.
		#
		#
		make_dir (zip_buffer_2, domain_directory);
		
		
		#
		#
		#	Destory GridFS Documents
		#
		#
		destroy_novella ({ "_id": treasure ["novella"] });
		
		#
		#
		#	Destory Vernacular Document
		#
		#
		destroy_vernacular_document ({
			"sieve": {
				"domain": domain
			}
		});
		
		return [ "victory", "" ]