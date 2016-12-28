## Collage Generator

These scripts are used for creating collage of the best and worst thumbnails.

prepare_data.py creates text files with sorted list of thumbnails which will be included in collage.

create_collage.sh creates collages.

## Usage

To use this script you have to edit some variables

In prepare_data.py:
 * IMG_PATH - path to directory with images
 * IMG_FILE_SOURCE - text file with sorted images
 * IMG_FILE_TARGET - output file
 * MAX_IMG - maximum number of images
 * ONE_IMG_PER_VIDEO - true if you want to have only one (better) image per video in collage (two images exists: preferred and beginning)

In create_collage.sh:
 * no changes required

<code>python prepare_data.py</code>

<code>./create_data.py IMG_FILE_TARGET</code>

where IMG_FILE_TARGET is the file created by the first script (prepare_data.py).

