## Popularity Sort

These scripts are used for sorting thumbnails based on the output of the last net's layer.

convert.py is used for converting binaryproto files to npy files.

popularity_thumb_sort.py is used for rating and sorting thumbnails.

## Usage

<code>python convert.py in.binaryproto out.npy</code>

Before running popularity_thumb_sort.py you have to modify some variables:
 * CAFFEMODEL - path to trained caffemodel
 * IMG_PATH - path to images

<code>python popularity_thumb_sort.py</code>

## Output

Five files will be generated:
 * file with thumbnails and calculated scores;
 * file with thumbnails and calculated POPULAR scores sorted;
 * file with thumbnails sorted by POPULAR scores;
 * file with thumbnails and calculated UNPOPULAR socres sorted;
 * file with thumbnails sorted by UNPOPULAR scores.
