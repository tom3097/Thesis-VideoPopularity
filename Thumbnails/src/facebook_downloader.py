#!/usr/bin/env python

__author__ = "Tomasz Bochenski"

import logging
import json
import os
import glob
import requests


if __name__ == '__main__':
    log_file = ''
    metadata_dir_path = ''
    metadata_file_pattern = ''
    result_dir_path = ''

    video_files = glob.glob(os.path.join(metadata_dir_path, metadata_file_pattern))

    logging.basicConfig(level=logging.INFO, propagate=False, filename=log_file, format='%(asctime)-15s %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    HEADERS = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    session = requests.session()

    logger.info('Start downloading thumbnails.')
    download_successful = 0
    download_failed = 0
    for v_file in video_files:
        successful_count = 0
        failed_count = 0
        logger.info('Downloading thumbnails for file: {}'.format(v_file))
        with open(v_file, 'r') as f:
            videos = json.load(f)
            for v in videos:
                os.makedirs(os.path.join(result_dir_path, v['id']), 755)
                got_beginning = False
                got_preferred = False
                for thumb in v['thumbnails']:
                    if got_beginning and got_preferred:
                        break
                    thumb_filename = os.path.join(result_dir_path, v['id'], thumb['id'])
                    beginning_thumb = None
                    preferred_thumb = None
                    if not got_beginning:
                        beginning_thumb = '{}_beginning.jpg'.format(thumb_filename)
                        got_beginning = True
                    if not got_preferred and thumb['is_preferred']:
                        preferred_thumb = '{}_preferred.jpg'.format(thumb_filename)
                        got_preferred = True
                    if beginning_thumb is None and preferred_thumb is None:
                        continue                   
                    try:
                        response = session.get(thumb["uri"], headers=HEADERS)
                        if not response.ok:
                            logger.error('Can not download thumbnail {} from video {}'.format(thumb['id'], v['id']))
                            download_failed += 1
                            failed_count += 1
                            continue
                        if beginning_thumb is not None:
                            with file(beginning_thumb, 'wb') as img_file:
                                img_file.write(response.content)
                        if preferred_thumb is not None:
                            with file(preferred_thumb, 'wb') as img_file:
                                img_file.write(response.content)
                        download_successful += 1
                        successful_count += 1
                    except Exception as e:
                        logger.error('Can not download thumbnail {} from video {}'.format(thumb['id'], v['id']))
                        download_failed += 1
                        failed_count += 1
                        if os.path.exists(thumb_filename):
                            os.remove(thumb_filename)
        logger.info('Successfully downloaded: {}, Failed: {}'.format(successful_count, failed_count))
    logger.info('Downloading thumbnails finished.')
    logger.info('Total thumbnails successfully downloaded: {}, failed: {}'.format(download_successful, download_failed))

