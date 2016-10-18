__author__ = "Tomasz Bochenski"


from json import dumps
from json import loads
from requests import request
from csv import reader
import logging


class YoutubeCrawler(object):
    def __init__(self, developer_key, channel_file, video_file, log_file):
        """Creates crawler for youtube

        Args:
            developer_key (string): Key used for creating requests to Youtube Data API.
            channel_file (string): Path to a file where metadata from channels will be saved.
            video_file (string): Path to a file where metadata from videos will be saved.
            log_file (string): Path to a file where logs will be saved.

        """

        self.developer_key = developer_key
        """string

        Key used for creating requests to Youtube Data API.
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

        Array that stores IDs of the channels which will be analyzed.
        """

        self.youtube_channels = []
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

        self.condition_array = ['2016-08', '2016-07', '2016-06']
        """array

        Array that stores permitted dates. Only them fulfill the conditions for filtering.
        """

        self.min_views = 300
        """int

        The minimum number of views that fulfill the condition for filtering.
        """


    def add_content_providers(self, csv_file):
        """Adds IDs of the channels to be analyzed.

        Args:
            csv_file (string): Path to a csv file with IDs of the channels.

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
        date = video_data['snippet']['publishedAt'][:7]
        if date not in self.condition_array:
            return False
        views = int(video_data['statistics']['viewCount'])
        if views < self.min_views:
            return False
        return True


    def analyze_channel(self, channel):
        """Gets metadata from the channel.
        Metadata obtained from the channel: 'id', 'statistics'.

        Args:
            channel (string): The id of the channel.

        Returns:
            dictionary: The dictionary with basic channel informations (keys: 'channel_UC',
            'channel_id', 'channel_likes')

        """
        parameters = {
            'part': 'id,statistics',
            'id': channel,
            'key': self.developer_key
        }
        url = 'https://www.googleapis.com/youtube/v3/channels'
        try:
            response = request(method='get', url=url, params=parameters)
        except Exception as e:
            raise Exception('Request for channel {} failed: {}'.format(channel, str(e)))
        j_response = loads(response.text)
        self.youtube_channels.append(j_response)
        try:
            with open(self.channel_file, 'w') as f:
                f.write(dumps(self.youtube_channels, indent=4))
        except Exception as e:
            raise Exception('Can not save youtube channels to file: {}'.format(str(e)))
        channel_info = {
            'channel_UC': channel,
            'channel_id': j_response['items'][0]['id'],
            'channel_likes': j_response['items'][0]['statistics']['subscriberCount']
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
        self.logger.info('Saving finished')


    def get_channel_video_ids(self, channel, page_token):
        """Gets ids of the videos from the channel.

        Args:
            channel (string): The id of the channel.
            page_token (string): Token for currently analyzed page ot the request.

        Returns:
            dictionary: The dictionary with ids of the videos.

        """
        parameters = {
            'part': 'id',
            'publishedAfter': '2016-06-01T00:00:00Z',
            'publishedBefore': '2016-08-31T00:00:00Z',
            'order': 'date',
            'maxResults': 50,
            'pageToken': page_token,
            'type': 'video',
            'channelId': channel,
            'key': self.developer_key
        }
        url = 'https://www.googleapis.com/youtube/v3/search'
        try:
            response = request(method='get', url=url, params=parameters)
        except Exception as e:
            raise Exception('Request for videos from channel {} with page token {} failed: {}'.format(channel, page_token, str(e)))
        j_response = loads(response.text)
        return j_response


    def get_channel_video_data(self, id_list):
        """Gets metadata from the videos.
        Metadata obtained from the video: 'id', 'snippet', 'statistics'.

        Args:
            id_list (array): The array with ids of the videos. For each of the videos included in the
            array metadata will be obtained.

        Returns:
            array: The array with metadata from the videos.

        """
        parameters = {
            'part': 'id,snippet,statistics',
            'id' : ','.join(id_list),
            'max_Results': 50,
            'key': self.developer_key
        }
        url = 'https://www.googleapis.com/youtube/v3/videos'
        try:
            response = request(method='get', url=url, params=parameters)
        except Exception as e:
            raise Exception('Request for videos data failed: {}'.format(str(e)))
        j_response = loads(response.text)
        return j_response


    def analyze_channel_videos(self, channel, channel_info):
        """Gets ids of the videos from the channel and metadata from videos which ids were obtained
        in the first step.

        Args:
            channel (string): The id of the chennel.
            channel_info (dictionary): The dictionary with basic channel informations (keys: 'channel_UC',
            'channel_id', 'channel_likes')

        """
        channel_videos = []
        integrity_array = []
        video_file = '{}_{}{}'.format(self.video_file_name, channel, self.video_file_extension)
        request_counter = 0
        total_channel_videos = 0
        page_token = ''
        while page_token is not None:
            video_ids = self.get_channel_video_ids(channel, page_token)
            if 'items' not in video_ids:
                break
            page_token = None
            if 'nextPageToken' in video_ids:
                page_token = video_ids['nextPageToken']
            id_list = []
            for v in video_ids['items']:
                id_list.append(v['id']['videoId'])
            try:
                video_data = self.get_channel_video_data(id_list)
            except Exception as e:
                self.logger.error(str(e))
                continue
            request_counter += 1
            for video_d in video_data['items']:
                if self.perform_filtering(video_d):
                    if video_d['id'] in integrity_array:
                        continue
                    integrity_array.append(video_d['id'])
                    video_d.update(channel_info)
                    channel_videos.append(video_d)
                    total_channel_videos += 1
                    self.total_videos += 1
            if request_counter == self.max_requests_per_save:
                request_counter = 0
                self.save_videos(channel_videos, video_file, total_channel_videos)
        self.save_videos(channel_videos, video_file, total_channel_videos)
        self.logger.info('Total videos: {}'.format(self.total_videos))


    def start(self):
        """Starts crawling.

        """
        self.logger.info('Start crawling.')
        for channel in self.channels_array:
            self.logger.info('Analyzing channel: {}'.format(channel))
            try:
                channel_info = self.analyze_channel(channel)
                self.analyze_channel_videos(channel, channel_info)
            except Exception as e:
                self.logger.error(str(e))
        self.logger.info('Crawling finished.')



if __name__ == '__main__':
    developer_key = ''
    channel_file = ''
    video_file = ''
    log_file = ''
    content_file = ''

    youtube_crawler = YoutubeCrawler(developer_key, channel_file, video_file, log_file)
    youtube_crawler.add_content_providers(content_file)
    youtube_crawler.start()
