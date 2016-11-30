## Video Crawlers

This scripts are used for crawling data from Facebook, Youtube and Dailymotion.


### Crawling data from Facebook

Requirements:

Facebook Graph API must by installed.

Before running script run_Facebook.php add some informations in the main section:
 * APP_ID: facebook application id
 * APP_SECRET: facebook application secret
 * TOKEN: token obtaine from facebook
 * page_file: path to a file where metadata from facebook pages will be saved.
 * video_file: pattern for a file where metadata from videos will be saved.
 * log_dir: path to a file where the logs will be saved.
 * content_file: path to a file with content providers informations (ids)

After that just type:

<code>php run_Facebook.php</code>

### Crawling data from Youtube

Requirements:

Youtube Data API

Before running script run_Youtube.py add some informations in the main section:
 * developer_key: key obtained from youtube API
 * channel_file: path to a file where metadata from youtube channels will be saved.
 * video_file: pattern for a file where metadata from videos will be saved.
 * log_file: path to a file where the logs will be saved.
 * content_file: path to a file with content providers informations (ids)

After that just type:

<code>python run_Youtube.py</code>

### Crawling data from Dailymotion

Requirements:

Dailymotion API

Before running script run_Dailymotion.py add some informations in the main section:
 * user_file: path to a file where metadata from dailymotion users will be saved.
 * video_file: pattern for a file where metadata from videos will be saved.
 * log_file: path to a file where the logs will be saved.
 * content_file: path to a file with content providers informations (ids)

After that just type:

<code>python run_Dailymotion.py</code>

## Output

As a result directory with video's metadata will be created.
