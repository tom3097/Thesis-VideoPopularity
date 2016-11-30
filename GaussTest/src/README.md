## Histogram generators

This scripts are used for generating histograms based on the number of the normalized points.

## Usage

To run this script type:

<code>Rscript gauss_[dailymotion/facebook/youtube].R --date DATE --directory DIRECTORY --video_pattern VIDEO_PATTERN</code>

Where:
 * DATE: the date when the videos were published (format: yyyy-mm); only videos that have the same yyyy-mm of the publication will be included in the histogram.
 * DIRECTORY: path to the directory with data obtained during crawling.
 * VIDEO_PATTERN: file name's pattern used for saving data during crawling.

## Output

Png image - histogram will be created as an output.
