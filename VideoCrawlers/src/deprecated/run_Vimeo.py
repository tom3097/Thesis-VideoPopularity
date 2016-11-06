__author__ = "Tomasz Bochenski"


from csv import reader
from vimeo import VimeoClient
from json import dumps
import logging

class VimeoCrawler(object):
    def __init__(self, vimeo_data, channel_file, video_file, log_file):
        """Creates crawler for dailymotion.

        Args:
            vimeo_data (dictionary): Dictionary with vimeo client informations: accessToken, clientId, clientSecret.
            channel_file (string): Path to a file where metadata from channels will be saved.
            video_file (string): Path to a file where metadata from videos will be saved.
            log_file (string): Path to a file where logs will be saved.

        """

        self.v = VimeoClient(token=vimeo_data['accessToken'], key=vimeo_data['clientId'], secret=vimeo_data['clientSecret'])
        """VimeoClient

        Object used for sending requests and getting responses using Vimeo API.
        """

        self.channel_file = channel_file
        """string

        Path to a file where metadata from channels will be saved.
        """

        dot_idx = video_file.rfind('.')
        self.video_file_name = video_file[:dot_idx]
        """string

        Path to a file without extension where metadata from videos will be saved.
        """

        self.video_file_extension = video_file[dot_idx:]
        """string

        Extension for the path to a file where metadata from videos will be saved.
        """

        logging.basicConfig(level=logging.INFO, propagate=False, filename=log_file, format='%(asctime)-15s %(message)s')
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)
        """Logger

        Object used for logging.
        """

        self.channels_array = []
        """array

        Array that stores names of the channels which will be analyzed.
        """

        self.vimeo_channels = []
        """array

        Array that stores metadata from channels.
        """

        self.total_videos = 0
        """int

        The total number of metadata from videos successfully obtained during crawling.
        """

        self.max_requests_per_save = 10
        """int

        The number of requests after which metadata from videos will be saved to a file.
        """

        self.condition_array = ['2016-08', '2016-07', '2016-06', '2016-05', '2016-04', '2016-03',
        '2016-02', '2016-01', '2015-12', '2015-11', '2015-10', '2015-09']
        """array

        Array that stores permitted dates. Only them fulfill the conditions for filtering.
        """

        self.min_views = 0
        """int

        The minimum number of views that fulfill the condition for filtering.
        """


    def add_content_providers(self, csv_file):
        """Adds names of the channels to be analyzed.

        Args:
            csv_file (string): Path to a csv file with names of the channels.

        """
        try:
            with open(csv_file, 'r') as f:
                data = reader(f)
                for row in data:
                    self.channels_array.append(row[1])
                self.channels_array.pop(0)
        except Exception as e:
            raise Exception('Can not read data from file: {}'.format(str(e)))


    def perform_filtering(self, video_data):
        """Performs filtering. Checks whether the video meets the conditions.

        Args:
            video_data (dictionary): The dictionary with video's metadata.

        Returns:
            boolean: True if video meets the conditions, False otherwise.

        """
        date = video_data['created_time'][:7]
        if date not in self.condition_array:
            return False
        views = video_data['stats']['plays']
        if views is None or views < self.min_views:
            return False
        return True


    def analyze_channel(self, channel):
        """Gets metadata from the channel.
        Metadata obtained from the channel: 'metadata', 'user.metadata'.

        Args:
            channel (string): The id of the channel.

        Returns:
            dictionary: The dictionary with basic channel informations (keys: 'channel_id',
            'channel_likes')

        """
        try:
            response = self.v.get('/channels/{}'.format(channel)).json()
            response = {
                'channel_id': channel,
                'channel_meta': response['metadata'],
                'user_meta': response['user']['metadata']
            }
        except Exception as e:
            raise Exception('Request for channel {} failed: {}'.format(channel, str(e)))
        self.vimeo_channels.append(response)
        try:
            with open(self.channel_file, 'w') as f:
                f.write(dumps(self.vimeo_channels, indent=4))
        except Exception as e:
            raise Exception('Can not save vimeo channels to file: {}'.format(str(e)))
        channel_info = {
            'channel_id': channel,
            'channel_likes': response['channel_meta']['connections']['users']['total']
        }
        return channel_info


    def save_videos(self, channel_videos, video_file, total_channel_videos):
        """Saves metadata from videos for currently analyzed channel to a file.

        Args:
            channel_videos (array): Array with metadata from videos for currently analyzed channel.
            video_file (string): Path to a file where metadata from videos for currently analyzed
            channel will be saved.
            total_channel_videos (int): The number of metadata from videos successfully obtained
            for currently analyzed channel.

        """
        self.logger.info('Saving to file...')
        self.logger.info('Total channel videos: {}'.format(total_channel_videos))
        try:
            with open(video_file, 'w') as f:
                f.write(dumps(channel_videos, indent=4))
        except Exception as e:
            raise Exception('Can not save videos to file.')
        self.logger.info('Saving finished.')


    def analyze_channel_videos(self, channel, channel_info):
        """Gets metadata from videos for currently analyzed channel.

        Args:
            channel (string): The id of the channel.
            channel_info (dictionary): The dictionary with basic channel informations (keys: 'channel_id',
            'channel_likes')

        """
        channel_videos = []
        integrity_array = []
        video_file = '{}_{}{}'.format(self.video_file_name, channel, self.video_file_extension)
        request_counter = 0
        total_channel_videos = 0
        fields = {
            'uri', 'name', 'description', 'link', 'duration',
            'width', 'height', 'language', 'created_time',
            'modified_time', 'privacy', 'pictures', 'tags',
            'stats', 'metadata', 'user.uri',
        }
        request = '/channels/{}/videos?fields={}&per_page=50&page=1&sort=date&direction=desc'.format(channel, ','.join(fields))
        while request is not None:
            try:
                response = self.v.get(request).json()
            except Exception as e:
                self.logger.error('Request for video data from channel {} failed: {}'.format(channel, str(e)))
                break
            if 'data' not in response:
                break
            request_counter += 1
            for video_d in response['data']:
                if self.perform_filtering(video_d):
                    if video_d['uri'] in integrity_array:
                        continue
                    integrity_array.append(video_d['uri'])
                    video_d.update(channel_info)
                    channel_videos.append(video_d)
                    total_channel_videos += 1
                    self.total_videos += 1
            if request_counter == self.max_requests_per_save:
                request_counter = 0
                self.save_videos(channel_videos, video_file, total_channel_videos)
            request = response['paging']['next']
        self.save_videos(channel_videos, video_file, total_channel_videos)
        self.logger.info('Total videos: {}'.format(self.total_videos))


    def start(self):
        """Starts crawling.

        """
        self.logger.info('Start crawling')
        for channel in self.channels_array:
            self.logger.info('Analyzing channel: {}'.format(channel))
            try:
                channel_info = self.analyze_channel(channel)
                self.analyze_channel_videos(channel, channel_info)
            except Exception as e:
                self.logger.error(str(e))
        self.logger.info('Crawling finished.')



if __name__ == '__main__':
    YOUR_ACCESS_TOKEN = ''
    YOUR_CLIENT_ID = ''
    YOUR_CLIENT_SECRET = ''
    vimeo_data = {
        'accessToken': YOUR_ACCESS_TOKEN,
        'clientId': YOUR_CLIENT_ID,
        'clientSecret': YOUR_CLIENT_SECRET
    }
    channel_file = ''
    video_file = ''
    log_file = ''
    content_file = ''

    vimeo_crawler = VimeoCrawler(vimeo_data, channel_file, video_file, log_file)
    crawler.add_content_providers(content_file)
    crawler.start()
