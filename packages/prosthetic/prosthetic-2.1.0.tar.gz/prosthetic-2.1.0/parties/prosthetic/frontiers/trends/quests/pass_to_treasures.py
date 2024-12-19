

'''

'''

#/
#
import ast
from pprint import pprint
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

from bson import ObjectId

def pass_to_treasures (packet):
	domain = packet [ "domain" ]

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