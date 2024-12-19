

''''
	from prosthetic.mixes.zipping.make_zip import make_zip
	make_zip ({
		"directory_path": directory_path
	});
"'''


import shutil
import io
import os



def find_temporary_file ():
	temp_archive_foundation = '/tmp/temp_archive'
	
	loop_numeral = 0;
	while (loop_numeral <= 10000):
		temp_archive = temp_archive_foundation + "." + str (loop_numeral);
		temp_archive_zip = temp_archive_foundation + ".zip"
	
		if os.path.exists (temp_archive_zip):
			loop_numeral = loop_numeral + 1;
			continue;
		else:
			break;

	return temp_archive


#
#
#	This creates: /tmp/temp_archive.zip
#
#
def make_zip (packet):
	directory_path = packet ["directory_path"]
	zip_path_without_extension = packet ["zip_path_without_extension"]

	#
	# 	This makes a temporary file 
	# 	in memory (avoids saving to disk)
	#
	byte_io = io.BytesIO ()

	# Use shutil.make_archive to create a zip file in memory (in a temporary file)
	temp_archive = zip_path_without_extension;
	temp_archive_zip = temp_archive + ".zip"
	shutil.make_archive (temp_archive, 'zip', directory_path)

	# print ("made:", temp_archive)

	# Open the temp archive and read it into memory
	with open (temp_archive_zip, 'rb') as f:
		byte_io.write (f.read ())

	#
	#
	#	This destroys the temp archive.
	#
	#
	# os.remove (temp_archive_zip)
	# print ("destroyed:", temp_archive)


	byte_io.seek (0)
	return byte_io.read ()