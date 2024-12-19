
#/
#
from ._quests.itemize import itemize_treasures
from prosthetic.treasures.pass_to_trends import pass_treasure_to_trends
#
#
import click
#
#
import os
#
#\

def treasures_clique ():
	@click.group ("treasures")
	def group ():
		pass
		
		
	@group.command ("itemize")
	def command_itemize ():		
		itemize_treasures ({
			"print_to_shell": "yes"
		})
		
		
		
	''''
		prosthetic_1 treasures pass --domain "health.1" --path "./health.1" --version freshest
	"'''
	''''
		"directories": {
			"freshest": ""
		} 
	"'''
	@group.command ("pass", help = """
		
		This is for passing a treasure to the trends.
		
	""")
	@click.option ('--domain', required = True)
	def command_insert_directory (domain):
		CWD = os.getcwd ()
	
		#
		#	moves:
		#		1. tar the treasure with "ships"
		#
		print ("command_insert_directory")
		
		
		
		pass_treasure_to_trends ({
			"domain": domain
		})
		
		return;

	return group




#



