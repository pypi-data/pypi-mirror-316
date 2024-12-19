


'''
	from prosthetic.adventures.monetary.venture import flask_venture
	flask_venture ()
'''

from ._controls.on import turn_on
from ._controls.off import turn_off
from ._controls.is_on import is_on

def flask_venture ():
	return {
		"name": "flask",
		"kind": "task",
		"turn on": {
			"adventure": turn_on,
		},
		"turn off": turn_off,
		"is on": is_on
	}