#!/usr/bin/env python

import sys
import random

train_txt_file = sys.argv[1]
groups_number = int(sys.argv[2])

videos = {}

lines = []

groups = groups_number * [None]
for x in xrange(groups_number):
    groups[x] = []

with open(train_txt_file, 'r') as f:
    lines = f.read().splitlines()

for l in lines:
    _, label = l.split()
    if label not in videos:
        videos[label] = {}
    id = l[0:l.find('/')]
    if id not in videos[label]:
        videos[label][id] = []
    videos[label][id].append(l)

for k in videos.keys():
    group_size = int(len(videos[k].keys())/float(groups_number))
    kk = videos[k].keys();
    random.shuffle(kk)
    for x in xrange(groups_number-1):
        for i in xrange(x*group_size, (x+1)*group_size):
            groups[x].append(videos[k][kk[i]])
    for i in xrange((groups_number-1)*group_size, len(videos[k].keys())):
        groups[groups_number-1].append(videos[k][kk[i]])

for x in xrange(groups_number):
    to_save = []
    for v in groups[x]:
        for e in v:
            to_save.append(e)
    random.shuffle(to_save)
    filename = 'group{}.txt'.format(x)
    with open(filename, 'w') as f:
        str = '\n'.join(to_save)
        f.write(str)

