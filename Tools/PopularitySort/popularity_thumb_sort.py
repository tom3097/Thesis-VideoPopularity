#!/usr/bin/python

import caffe
import numpy as np
import os

# paths
DEPLOY_ARCH = 'deploy_2.prototxt'
CAFFEMODEL = '/home/tomasz/Documents/Thesis/Nets/Facebook/PrefBegin_2_vol3/facebook_solv4_iter_16000.caffemodel'
IMG_MEAN = 'imagenet_mean.npy'
IMG_PATH = '/home/tomasz/Documents/Thesis/Thumbnails/facebook/results/'
VAL_IMG_FILE = 'val_thumb_2.txt'

# set gpu mode
caffe.set_device(0)
caffe.set_mode_gpu()


# create net
net = caffe.Net(DEPLOY_ARCH, CAFFEMODEL, caffe.TEST)


# load input and configure preprocessing
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape })
transformer.set_mean('data', np.load(IMG_MEAN).mean(1).mean(1))
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))
transformer.set_raw_scale('data', 255.0)

# respahe blob
net.blobs['data'].reshape(1,3,227,227)

data = []
vid_results = []

with open(VAL_IMG_FILE, 'r') as f:
	data = f.read().splitlines()

# calculate score for each image
for video_img in data:
	vid_img_name = video_img.split()[0]
	try:
		img = caffe.io.load_image(os.path.join(IMG_PATH, vid_img_name))
	except Exception as e:
		print('Exception occured: %s' % str(e))
		continue
	net.blobs['data'].data[...] = transformer.preprocess('data', img)
	out = net.forward()
	vid_results.append( (vid_img_name, out['fc8_2'][0].copy()) )

# save calculated scores
with open('unordered_scores.txt', 'w') as f:
	for result in vid_results:
		f.write('%s: %s\n' % (result[0], result[1]))

# sort images: the most popular
most_popular = sorted(vid_results, key=lambda x:x[1][1], reverse=True)

# save sorted images
with open('popular_sorted_score.txt', 'w') as f:
	for result in most_popular:
		f.write('%s: %s\n' % (result[0], result[1][1]))

with open('popular_sorted.txt', 'w') as f:
	for result in most_popular:
		f.write('%s\n' % result[0])

# sort images: the most unpopular
most_unpopular = sorted(vid_results, key=lambda x:x[1][0], reverse=True)

# save sorted images
with open('unpopular_sorted_score.txt', 'w') as f:
	for result in most_unpopular:
		f.write('%s: %s\n' % (result[0], result[1][0]))

with open('unpopular_sorted.txt', 'w') as f:
	for result in most_unpopular:
		f.write('%s\n' % result[0])
