import os

IMG_PATH = '/home/tomasz/Documents/Thesis/Thumbnails/facebook/results'
IMG_FILE_SOURCE = 'unpopular_sorted.txt'
IMG_FILE_TARGET = 'unpopular_prepared.txt'

ONE_IMG_PER_VIDEO = True

MAX_IMG = 400
img_count = 0
video_dict = {}

with open(IMG_FILE_SOURCE, 'r') as f:
    images = f.read().splitlines()

with open(IMG_FILE_TARGET, 'w') as f:
    for img in images:
        video_id = img.split('/')[0]
        if ONE_IMG_PER_VIDEO and video_id in video_dict:
            continue
        video_dict[video_id] = None
        f.write(os.path.join(IMG_PATH, img))
        f.write('\n')
        img_count += 1
        if img_count >= MAX_IMG:
            break


