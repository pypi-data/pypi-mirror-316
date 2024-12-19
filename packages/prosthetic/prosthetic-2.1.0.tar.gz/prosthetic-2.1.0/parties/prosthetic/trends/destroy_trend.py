
''''
	from prosthetic.trends.destroy_trend import destroy_trend
	destroy_trend ({ "domain": domain });
"'''



from prosthetic.adventures.monetary.DB_prosthetic_trends.collection_vernacular.document.search_one import search_one_trend
	
from .novellas.document.destroy import destroy_novella
from .vernacular.document.destroy import destroy_vernacular_document
	
def destroy_trend (packet):
	domain = packet ["domain"]

	print ("destroy_trend:", domain);

	trend = search_one_trend ({
		"filter": {
			"domain": domain
		}
	});
	trend_novella_id = trend ["novella"]
	
	print ("destroy_trend trend:", trend);
	

	destroy_novella ({ "_id": trend_novella_id });
	
	destroy_vernacular_document ({
		"sieve": {
			"domain": domain
		}
	});