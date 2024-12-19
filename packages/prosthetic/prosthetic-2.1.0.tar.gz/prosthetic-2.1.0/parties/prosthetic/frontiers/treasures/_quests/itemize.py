
'''
	from prosthetic.frontiers.treasures._quests.itemize import itemize_treasures
	treasures = itemize_treasures ()
'''


import os
from prosthetic._essence import retrieve_essence

from pprint import pprint

from os.path import normpath
import json

def list_directories (directory):
	directories = []
	anomalies = []

	places = os.listdir (directory)
	for place in places:
		full_path = os.path.join (directory, place)
		
		if (os.path.isdir (full_path)):
			directories.append (place)
		else:
			raise Exception (f"A non-directory was found at: { place }")

	return {
		"directories": directories,
		"anomalies": anomalies
	}
	
def split_last_substring (string):
	try:
		last_dot_index = string.rfind ('.')

		if last_dot_index != -1:
			part_before = string [:last_dot_index]
			part_after = string [last_dot_index + 1:]
			return [ part_before, part_after ]
		
		raise Exception (f"A non-dot directory name was found: { string }")
	except Exception as E:
		print ("split_last_substring exception:", E)
		
	return;

def search_for_prosthetic_JSON (packet):
	full_path = packet ["full_path"]
	
	possible_bracket_path = os.path.normpath (os.path.join (full_path, "Prosthetic.JSON"));
	
	
	bracket = ""
	try:
		
		with open (possible_bracket_path, 'r') as Reader:
			bracket = json.loads (Reader.read ())
			return bracket;
	
	except Exception as E:
		print ("search_for_prosthetic_JSON exception:", E)
		# bracket = E;
		
	return bracket

def itemize_treasures (packet = {}):
	essence = retrieve_essence ()
	treasures_path = essence ["treasures"] ["path"]

	print_to_shell = "no"
	if (type (packet) == dict):
		if ("print_to_shell" in packet):
			print_to_shell = packet ["print_to_shell"]

	proceeds = list_directories (treasures_path)
	directories = proceeds ["directories"]
	anomalies = proceeds ["anomalies"]
	
	treasures = []
	for directory in directories:
		#print ("directory:", directory)
		
		print ("directory:", directory)
		
		#
		#
		#	Search for "Prosthetic.JSON"
		#
		#
		bracket = search_for_prosthetic_JSON ({
			"full_path": os.path.join (treasures_path, directory)
		});
		
		domain_split = split_last_substring (directory)
		treasures.append ({
			"domain": directory,
			"domain split": domain_split,
			"bracket": bracket
		})
		
		
	if (print_to_shell == "yes"):
		pprint (treasures)	
		


	return treasures