## Thumbnails downloaders

This scripts are used for downloading frames for the given videos.

## Usage

Requirements:

This script requires Celery to be installed.

To use this script you have to edit some variables in the main section:
 * log_file: path to a file where the logs will be saved.
 * metadata_dir_path: path to the directory with video's data obtained during crawling.
 * metadata_file_pattern: file name's pattern used for saving data during crawling. 
 * result_dir_path: path to a directory where the thumbnails will be saved.

After that just type

<code>python [dailymotion/facebook/youtube]_FramesDownloader.py</code>

If you want to run downloading in the background type:

<code>supervisord</code>

<code>python run_FramesDownloader.py &</code>

<code>disown</code>

## Output

As a result directory with frames will be created.
