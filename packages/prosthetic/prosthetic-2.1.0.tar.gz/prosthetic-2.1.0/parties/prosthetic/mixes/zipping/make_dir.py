




''''
	from prosthetic.mixes.zipping.make_dir import make_dir
	make_dir (zip_bytes, output_directory);
"'''

import os
import io

import zipfile


#
#
#
#
#
def make_dir (zip_bytes, output_directory):
    os.makedirs (output_directory, exist_ok = True)

    with zipfile.ZipFile (io.BytesIO (zip_bytes), 'r') as zip_ref:
        zip_ref.extractall (output_directory)

    print (f"Contents extracted to {output_directory}")
