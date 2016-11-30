## Popularity Ranks Counters

This scripts are used for calculating limit values between each popularity class. It is assumed that popularity scores are calculated from formula:
<code> points = log2((number_of_views+1)/number_of_followers)</code>

## Usage

To use this script you have to edit / fill in some variables.
 * Line 3, DEPTH: refers to the number of classes. Number of classes is multiplicity of 2, and the DEPTH is equal to log(number_of_classes). So if you want to split data into 2 classed, DEPTH would be 1, if you want to split data into 8 classes - DEPTH would be 3.
 * Line 5, video_directory: it is the path to the directory with the video's data obtained during crawling.
 * Line 6, pattern: file name's pattern used for saving data from crawling.

## Output

Script will generate json file, where each key represents the time when videos were published and values are arrays with limit values between each popularity class.
