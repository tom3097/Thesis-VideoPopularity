__author__ = "Tomasz Bochenski"


import logging
import json
import os
import glob
import requests

class FacebookImagesDwnl(object):
    def __init__(self, log_file, metadata_dir_path, metadata_file_pattern, result_dir_path):
        """Creates facebook images downloader.

        Args:
            log_file (string): Path to a file where logs will be saved.
            metadata_dir_path (string): Path to a directory where facebook metadata are stored.
            metadata_file_pattern (string): Facebook metadata files pattern.
            result_dir_path (string): Path to a root directory where images will be saved.

        """

        self.result_dir_path = result_dir_path
        """string

        Path to a root directory where images will be saved.
        """

        self.video_files = glob.glob(os.path.join(metadata_dir_path, metadata_file_pattern))
        """array

        Array of paths to facebook metadata files.
        """

        logging.basicConfig(level=logging.INFO, propagate=False, filename=log_file, format='%(asctime)-15s %(message)s')
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)
        """Logger

        Object used for logging.
        """

        self.HEADERS = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        """dictionary

        Headers used for performing http requests.
        """

        self.session = requests.session()
        """Session

        Object used for performing http requests.
        """

        self.download_successful = 0
        """Integer

        The total number of images successfully obtained.
        """

        self.download_failed = 0
        """Integer

        The total number of downloads which failed.
        """

        self.successful_count = None
        """Integer

        The total number of images successfully obtained for currently analyzed file.
        """

        self.failed_count = None
        """Integer

        The total number of downloads which failed for currently analyzed file.
        """


    def download_beginning_thumbnail(self, video_data):
        """Download a beginning thumbnail for a given video.

        Args:
            video_data (dictionary): Dictionary with all video informations obtained during crawling.

        """   
        filename = os.path.join(self.result_dir_path, video_data['id'], '{}_beginning.jpg'.format(video_data['thumbnails'][0]['id']))
        try:
            response = self.session.get(video_data['thumbnails'][0]['uri'], headers=self.HEADERS)
            if not response.ok:
                self.logger.error('Can not download beginning thumbnail from video {}'.format(video_data['id']))
                self.download_failed += 1
                self.failed_count += 1
            else:
                with file(filename, 'wb') as img_file:
                    img_file.write(response.content)
                self.download_successful += 1
                self.successful_count += 1
        except Exception as e:
            self.logger.error('Can not download beginning thumbnail from video {}: {}'.format(video_data['id'], str(e)))
            self.download_failed += 1
            self.failed_count += 1
            if os.path.exists(filename):
                os.remove(filename)


    def download_pref_thumbnail(self, video_data):
        """Download a preferred thumbnail for a given video.

        Args:
            video_data (dictionary): Dictionary with all video informations obtained during crawling.

        """
        filename = os.path.join(self.result_dir_path, video_data['id'], '{}_thumbnail.jpg')
        try:
            for thumb in video_data['thumbnails']:
                if not thumb['is_preferred']:
                    continue
                response = self.session.get(thumb["uri"], headers=self.HEADERS)
                if not response.ok:
                    self.logger.error('Can not download preferred thumbnail from video {}'.format(video_data['id']))
                    self.download_failed += 1
                    self.failed_count += 1
                else:
                    filename = filename.format(thumb['id'])
                    with file(filename, 'wb') as img_file:
                        img_file.write(response.content)
                    self.download_successful += 1
                    self.successful_count += 1
                return
        except Exception as e:
            self.logger.error('Can not download preferred thumbnail from video {}: {}'.format(video_data['id'], str(e)))
            self.download_failed += 1
            self.failed_count += 1
            if os.path.exists(filename):
                os.remove(filename)


    def start(self):
        """Starts downloading images.

        """
        self.logger.info('Start downloading thumbnails.')
        for v_file in self.video_files:
            self.successful_count = 0
            self.failed_count = 0
            self.logger.info('Downloading thumbnails for file: {}'.format(v_file))
            with open(v_file, 'r') as f:
                videos = json.load(f)
                for v in videos:
                    os.makedirs(os.path.join(self.result_dir_path, v['id']))
                    self.download_beginning_thumbnail(v)
                    self.download_pref_thumbnail(v)
            self.logger.info('Successfully downloaded: {}, Failed: {}'.format(self.successful_count, self.failed_count))
        self.logger.info('Total thumbnails successfully downloaded: {}, failed: {}'.format(self.download_successful, self.download_failed))
        self.logger.info('Downloading thumbnails finished.')



if __name__ == '__main__':
    log_file = ''
    metadata_dir_path = ''
    metadata_file_pattern = ''
    result_dir_path = ''

    facebook_images_dwnl = FacebookImagesDwnl(log_file, metadata_dir_path, metadata_file_pattern, result_dir_path)
    facebook_images_dwnl.start()
