__author__ = "Tomasz Bochenski"

from tasks import download_frames
import os
import glob
import json
import logging
import time

class DailymotionFramesDwnl(object):
    def __init__(self, log_file, metadata_dir_path, metadata_file_pattern, result_dir_path):
        """Creates dailymotion images downloader.

        Args:
            log_file (string): Path to a file where logs will be saved.
            metadata_dir_path (string): Path to a directory where dailymotion metadata are stored.
            metadata_file_pattern (string): Dailymotion metadata files pattern.
            result_dir_path (string): Path to a root directory where images will be saved.
        """

        self.video_ids = []
        """Array

        Array with video ids.
        """

        self.TASK_ARRAY_SIZE = 10
        """Integer

        The number of tasks that can run parallel.
        """

        self.tasks_array = [ None ] * self.TASK_ARRAY_SIZE
        """Array

        Array with tasks.
        """

        self.video_files = glob.glob(os.path.join(metadata_dir_path, metadata_file_pattern))
        """Array

        Array of paths to dailymotion metadata files.
        """

        self.result_dir_path = result_dir_path
        """string

        Path to a root directory where images will be saved.
        """

        logging.basicConfig(level=logging.INFO, propagate=False, filename=log_file, format='%(asctime)-15s %(message)s')
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)
        """Logger

        Object used for logging.
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

        self.TASK_ARRAY_SIZE = 10
        """Integer

        The number of tasks that can run parallel.
        """


    def complete_video_ids(self, video_file):
        """Deletes currently stored video ids and adds ids from video_file file.

        Args:
            video_file (string): Path to a file where dailymotion metadata are stored.

        """
        self.video_ids = []
        with open(video_file, 'r') as f:
            v_data = json.load(f)
            for v in v_data:
                self.video_ids.append(v['id'])


    def handle_result(self, task_index):
        """Handles the result of the task with index task_index in tasks_array.

        Args:
            task_index (int): The index of the task which is to be handled.

        """
        try:
            v_id = self.tasks_array[task_index].get()
            self.logger.info('Video id: %s analyzed', v_id)
            self.successful_count += 1
            self.download_successful += 1
        except Exception as e:
            self.logger.error('Error while downloading frames')
            self.failed_count += 1
            self.download_failed += 1


    def start(self):
        """Starts downloading frames

        """
        self.logger.info('Start downloading frames.')
        for v_file in self.video_files:
            self.logger.info('Downloading frames for file: {}'.format(v_file))
            self.complete_video_ids(v_file)
            self.successful_count = 0
            self.failed_count = 0
            for x in xrange(min(len(self.tasks_array), len(self.video_ids))):
                self.tasks_array[x] = download_frames.delay(self.video_ids[x], self.result_dir_path)    
            video_index = min(len(self.tasks_array), len(self.video_ids))
            task_index = 0
            while video_index < len(self.video_ids):
                if self.tasks_array[task_index].ready():
                    self.handle_result(task_index)
                    self.tasks_array[task_index] = download_frames.delay(self.video_ids[video_index], self.result_dir_path)
                    video_index += 1
                task_index = (task_index + 1) % self.TASK_ARRAY_SIZE
                if task_index == 0:
                    time.sleep(2)
            for x in xrange(min(len(self.tasks_array), len(self.video_ids))):
                while not self.tasks_array[x].ready():
                    time.sleep(2)
                self.handle_result(x)
            self.logger.info('Successfully downloaded: {}, Failed: {}'.format(self.successful_count, self.failed_count))
        self.logger.info('Total thumbnails successfully downloaded: {}, failed: {}'.format(self.download_successful, self.download_failed))
        self.logger.info('Downloading frames finished.')




if __name__ == '__main__':
    log_file = ''
    metadata_dir_path = ''
    metadata_file_pattern = ''
    result_dir_path = ''

    dailymotion_frames_dwnl = DailymotionFramesDwnl(log_file, metadata_dir_path, metadata_file_pattern, result_dir_path)
    dailymotion_frames_dwnl.start()
