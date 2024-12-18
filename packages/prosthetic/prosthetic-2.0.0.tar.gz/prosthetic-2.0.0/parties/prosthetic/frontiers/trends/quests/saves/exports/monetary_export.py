


#/
#
from prosthetic._essence import retrieve_essence
import prosthetic.mixes.procedure as procedure
#
#
import click
import rich
#
#
import pathlib
from os.path import dirname, join, normpath
import sys
import os
import time
#
#\


def export_documents (packet):
	version = packet ["version"]

	essence = retrieve_essence ()
	the_exports_path = essence ["trends"] ["monetary"] ["saves"] ["exports"] ["path"]
	URL = essence ["trends"] ["monetary"] ["URL"]
	monetary_databases = essence ["trends"] ["monetary"] ["saves"] ["exports"] ["databases"]
	
	print ("monetary_databases:", monetary_databases)
	
	already_exists = []
	for monetary_database in monetary_databases:
		database_name = monetary_databases [ monetary_database ] ["alias"]
		database_collections = monetary_databases [ monetary_database ] ["collections"]
		
		for collection in database_collections:
			# name = database_name + "." + collection + ".export"
			name = collection + ".export"
			export_path = str (normpath (join (
				the_exports_path, 
				version,
				database_name, 
				name
			)))
			if (os.path.exists (export_path) == True):
				already_exists.append (export_path)
				continue;
				
			process_strand = [
				"mongoexport",
				"--uri",
				URL,
				f"--db={ database_name }",
				f"--collection={ collection }",
				f"--out={ export_path }"
			]
			
			print (" ".join (process_strand))	
			
			procedure.go (
				script = process_strand
			)
			
			time.sleep (.25)
		
	chmod = f"chmod -R 777 '{ the_exports_path }'"
	
	print ("chmod:", chmod)
	
	os.system (chmod)

	rich.print_json (data = {
		"already_exists": already_exists
	})	

