



#/
#
import json
from os.path import exists, dirname, normpath, join
from urllib.parse import unquote
import threading
import time
from fractions import Fraction
#
#
import sanic
from sanic import Sanic
import sanic.response as sanic_response
#
#
from prosthetic._essence import retrieve_essence
from prosthetic.mixes.harbor.generate_inventory_paths import generate_inventory_paths
from prosthetic.frontiers.treasures._quests.itemize import itemize_treasures
from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.search import search_trends_vernacular
#

#
#\

#
#
#	Treasures
#
#
from prosthetic.treasures.pass_to_trends import pass_treasure_to_trends


#
#
#	Trends
#
#
from prosthetic.trends.destroy_trend import destroy_trend
from prosthetic.trends.pass_trend_to_treasures import pass_trend_to_treasures
	

def guest_regions (vue_regions_packet):
	essence = retrieve_essence ()
	
	
	##/
	build_path = essence ["sveltnetics"] ["build_path"];
	the_index = build_path + "/index.html"
	the_assets = build_path + "/assets"
	
	front_inventory_paths = generate_inventory_paths (build_path)
	for front_path in front_inventory_paths:
		print ("front_path:", front_path)
		pass;
	##\
		
	
	app = vue_regions_packet ["app"]
	guest_addresses = sanic.Blueprint ("guest", url_prefix = "/")
	app.blueprint (guest_addresses)

	#/
	#
	#	Trends
	#
	#
	@guest_addresses.route ("/monetary/trends/itemize")
	async def monetary_trends_itemize (request):
		trends_vernacular = search_trends_vernacular ({
			"filter": {}
		})
		
		return sanic_response.json ({
			"trends": trends_vernacular
		}, status = 200)
	
	@guest_addresses.post ("/monetary/trend/delete")
	async def monetary_trend_delete (request):
		data = request.json;
		domain = data ["domain"];
		
		destroy_trend ({ "domain": domain });
		
		return sanic_response.json ({
			"status": ""
		}, status = 200)
	
	@guest_addresses.post ("/monetary/trends/trend_to_treasure")
	async def monetary_trends_trend_to_treasures (request):
		packet = request.json;
		
		domain = packet ["domain"];
		similar = []
		if ("similar" in packet):
			similar = packet ["similar"]
		
		#print ("data:", data)
		
		pass_trend_to_treasures ({
			"domain": domain
		});
	
		'''
		if (status != "victory"):
			print ("status:", [ status, result_notes ]);
			return sanic_response.json ({
				"status": status
			}, status = 600)
		
		print ("passed:", domain);
		'''
		
		return sanic_response.json ({
			"status": ""
		}, status = 200)
	#
	#\
	
	
	#/
	#
	#	Treasures
	#
	#
	@guest_addresses.route ("/monetary/treasures/itemize")
	async def monetary_treasures_itemize (request):

		treasures = itemize_treasures ()	
		print ("treasures:", treasures);
		
		
		return sanic_response.json ({
			"treasures": treasures
		}, status = 200)
	
	@guest_addresses.post ("/monetary/treasures/treasure_to_trend")
	async def monetary_treasures_treasure_to_trend (request):
		data = request.json;
		domain = data ["domain"];
		similar = data ["similar"];
	
		print ("domain:", domain);
		print ("data:", data);
		
	
		[ status, result_notes ] = pass_treasure_to_trends ({
			"domain": domain,
			"similar": similar
		});
		print ("status:", status);
		print ("result_notes:", result_notes);
		
		return sanic_response.json ({
			"status": status
		}, status = 200)
	#
	#\
	
	
	
	
	
	
	
	
	
	
	
	@guest_addresses.route ("/")
	async def home (request):
		return await sanic_response.file (the_index)
		

	@guest_addresses.route ("/<path:path>")
	async def assets_route (request, path):
		the_path = False
		
		try:
			the_path = f"{ path }"
			
			if (the_path in front_inventory_paths):
				content_type = front_inventory_paths [ the_path ] ["mime"]
				content = front_inventory_paths [ the_path ] ["content"]
				
				print ('found:', the_path)
				print ('content_type:', content_type)
				
				return sanic_response.raw (
					content, 
					content_type = content_type,
					headers = {
						"Custom-Header-1": "custom",
						"Cache-Control": "private, max-age=31536000",
						#"Expires": "0"
					}
				)
				
		except Exception as E:
			print ("E:", E)
		
			return sanic_response.json ({
				"note": "An anomaly occurred while processing.",
				"the_path": the_path
			}, status = 600)
			
		return await sanic_response.file (the_index)


	