__author__ = "Tomasz Bochenski"


from json import dumps
from dailymotion import Dailymotion
from csv import reader
from time import strftime
from time import localtime
import logging

class DailymotionCrawler(object):
    def __init__(self, user_file, video_file, log_file):
        """Creates crawler for dailymotion.

        Args:
            user_file (string): Path to a file where metadata from users will be saved.
            video_file (string): Path to a file where metadata from videos will be saved.
            log_file (string): Path to a file where logs will be saved.

        """

        self.dm = Dailymotion()
        """Dailymotion

        Object used for sending requests and getting responses using Dailymotion API.
        """

        self.user_file = user_file
        """string

        Path to a file where metadata from users will be saved.
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

        self.users_array = []
        """array

        Array that stores names of the users which will be analyzed.
        """

        self.dailymotion_users = []
        """array

        Array that stores metadata from users.
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
        """Adds names of the users to be analyzed.

        Args:
            csv_file (string): Path to a csv file with names of the users.

        """
        try:
            with open(csv_file, 'r') as f:
                data = reader(f)
                for row in data:
                    self.users_array.append(row[1])
                self.users_array.pop(0)
        except Exception as e:
            raise Exception('Can not read data from file: {}'.format(str(e)))


    def perform_filtering(self, video_data):
        """Performs filtering. Checks whether the video meets the conditions.

        Args:
            video_data (dictionary): The dictionary with video's metadata.

        Returns:
            boolean: True if video meets the conditions, False otherwise.

        """
        date = video_data['created_time_readable'][:7]
        if date not in self.condition_array:
            return False
        views = video_data['views_total']
        if views < self.min_views:
            return False
        return True


    def analyze_user(self, user):
        """Gets metadata from the user.
        Metadata obtained from the user: 'followers_total', 'videos_total', 'videostar.bookmarks_total',
        'views_total'.

        Args:
            user (string): The name of the user.

        Returns:
            dictionary: The dictionary with basic user informations (keys: 'user_id', 'user_likes').

        """
        parameters = {
            'fields': 'id,followers_total,videos_total,videostar.bookmarks_total,views_total'
        }
        try:
            response = self.dm.get('/user/{}'.format(user), parameters)
        except Exception as e:
            raise Exception('Request for user {} failed: {}'.format(user, str(e)))
        response['name'] = user
        self.dailymotion_users.append(response)
        try:
            with open(self.user_file, 'w') as f:
                f.write(dumps(self.dailymotion_users, indent=4))
        except Exception as e:
            raise Exception('Can not save dailymotion users to file: {}'.format(str(e)))
        user_info = {
            'user_id': response['id'],
            'user_likes': response['followers_total']
        }
        return user_info


    def save_videos(self, user_videos, video_file, total_user_videos):
        """Saves metadata from videos for currently analyzed user to a file.

        Args:
            user_videos (array): Array with metadata from videos for currently analyzed user.
            video_file (string): Path to a file where metadata from videos for currently analyzed
            user will be saved.
            total_user_videos (int): The number of metadata from videos successfully obtained
            for currently analyzed user.

        """
        self.logger.info('Saving to file...')
        self.logger.info('Total user videos: {}'.format(total_user_videos))
        try:
            with open(video_file, 'w') as f:
                f.write(dumps(user_videos, indent=4))
        except Exception as e:
            raise Exception('Can not save videos to file.')
        self.logger.info('Saving finished.')


    def analyze_user_videos(self, user, user_info):
        """Gets metadata from videos for currently analyzed user.

        Args:
            user (string): The id of the user.
            user_info (dictionary): The dictionary with basic user informations (keys: 'user_id',
            'user_likes').

        """
        user_videos = []
        integrity_array = []
        video_file = '{}_{}{}'.format(self.video_file_name, user, self.video_file_extension)
        request_counter = 0
        total_user_videos = 0
        video_fields = {
            'id', 'title', 'thumbnail_url', 'tags', 'owner.id',
            'allow_comments', 'comments_total', 'bookmarks_total',
            'available_formats', 'views_last_day', 'views_last_hour',
            'views_last_month', 'views_last_week', 'views_total',
            'country', 'created_time', 'duration', 'embed_url',
            'filmstrip_60_url','language', 'description',
            'sprite_320x_url', 'aspect_ratio', 'url',
        }
        page = 1
        has_more = True
        while page <= 100 and has_more:
            parameters = {
                'fields': ','.join(video_fields),
                'page': str(page),
                'limit': '100',
                'created_after': '2016-06-01T00:00:00Z',
                'created_before': '2016-08-31T00:00:00Z'
            }
            page += 1
            try:
                response = self.dm.get('/user/{}/videos'.format(user), parameters)
            except Exception as e:
                self.logger.error('Request for video data from user {} failed: {}'.format(user, str(e)))
                continue
            if 'list' not in response:
                break
            request_counter += 1
            for video_d in response['list']:
                video_d['created_time_readable'] = strftime('%Y-%m-%d %H:%M:%S', localtime(video_d['created_time']))
                if self.perform_filtering(video_d):
                    if video_d['id'] in integrity_array:
                        continue
                    integrity_array.append(video_d['id'])
                    video_d.update(user_info)
                    user_videos.append(video_d)
                    total_user_videos += 1
                    self.total_videos += 1
            if request_counter == self.max_requests_per_save:
                request_counter = 0
                self.save_videos(user_videos, video_file, total_user_videos)
            has_more = response['has_more']
        self.save_videos(user_videos, video_file, total_user_videos)
        self.logger.info('Total videos: {}'.format(self.total_videos))


    def start(self):
        """Starts crawling.

        """
        self.logger.info('Start crawling.')
        for user in self.users_array:
            self.logger.info('Analyzing user: {}'.format(user))
            try:
                user_info = self.analyze_user(user)
                self.analyze_user_videos(user, user_info)
            except Exception as e:
                self.logger.error(str(e))
        self.logger.info('Crawling finished.')



if __name__ == '__main__':
    user_file = ''
    video_file = ''
    log_file = ''
    content_file = ''

    dailymotion_crawler = DailymotionCrawler(user_file, video_file, log_file)
    dailymotion_crawler.add_content_providers(content_file)
    dailymotion_crawler.start()
