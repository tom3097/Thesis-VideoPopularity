## Train val files generators

Those scripts are used for creating train.txt and val.txt files. This files are used by create_imagenet.sh script in caffe/example/imagenet directory which creates lmdb files upon them. Lmdb files are used directly by the caffe when training and testing.

## Usage

To use this script you have to edit some variables in the main section:
 * metadata_dir_path: path to the directory with video's data obtained during crawling.
 * metadata_file_pattern: file name's pattern used for saving data during crawling. 
 * ranges_dict_file: path to a file created by Popularity Rank Counter.
 * images_directory: path to a file with images
 * image_pattern: file name's pattern used for saving images
 * train_factor: percentage of the data which will be used for training
 * train_output: output file's name for training data
 * val_output: output file's name for validation data

After that just type:

<code>python [dailymotion/facebook]_tv_gen.py</code> 

## Output

Two files will be created, one for train data and one for validation data.
