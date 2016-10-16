#!/bin/bash

FACEBOOK_META=""
YOUTUBE_META=""
DAILYMOTION_META=""
VIMEO_META=""

FACEBOOK_PATTERN=""
YOUTUBE_PATTERN=""
DAILYMOTION_PATTERN=""
VIMEO_PATTERN=""

echo "Generating histograms for facebook."

Rscript gauss_facebook.R --directory $FACEBOOK_META --video_pattern $FACEBOOK_PATTERN --date 2016-08
echo "Histogram for: 2016-08 created."

Rscript gauss_facebook.R --directory $FACEBOOK_META --video_pattern $FACEBOOK_PATTERN --date 2016-07
echo "Histogram for: 2016-07 created."

Rscript gauss_facebook.R --directory $FACEBOOK_META --video_pattern $FACEBOOK_PATTERN --date 2016-06
echo "Histogram for: 2016-06 created."

echo "Generating histograms for youtube."

Rscript gauss_youtube.R --directory $YOUTUBE_META --video_pattern $YOUTUBE_PATTERN --date 2016-08
echo "Histogram for: 2016-08 created."

Rscript gauss_youtube.R --directory $YOUTUBE_META --video_pattern $YOUTUBE_PATTERN --date 2016-07
echo "Histogram for: 2016-07 created."

Rscript gauss_youtube.R --directory $YOUTUBE_META --video_pattern $YOUTUBE_PATTERN --date 2016-06
echo "Histogram for: 2016-06 created."

echo "Generating histograms for dailymotion."

Rscript gauss_dailymotion.R --directory $DAILYMOTION_META --video_pattern $DAILYMOTION_PATTERN --date 2016-08
echo "Histogram for: 2016-08 created."

Rscript gauss_dailymotion.R --directory $DAILYMOTION_META --video_pattern $DAILYMOTION_PATTERN --date 2016-07
echo "Histogram for: 2016-07 created."

Rscript gauss_dailymotion.R --directory $DAILYMOTION_META --video_pattern $DAILYMOTION_PATTERN --date 2016-06
echo "Histogram for: 2016-06 created."

echo "Generating histograms for vimeo."

Rscript gauss_vimeo.R --directory $VIMEO_META --video_pattern $VIMEO_PATTERN --date 2016-08,2016-07,2016-06,2016-05
echo "Histogram for: 2016-08 2016-07 2016-06 2016-05 created."

Rscript gauss_vimeo.R --directory $VIMEO_META --video_pattern $VIMEO_PATTERN --date 2016-04,2016-03,2016-02,2016-01
echo "Histogram for: 2016-04 2016-03 2016-02 2016-01 created."

Rscript gauss_vimeo.R --directory $VIMEO_META --video_pattern $VIMEO_PATTERN --date 2015-12,2015-11,2015-10,2015-09
echo "Histogram for: 2015-12 2015-11 2015-10 2015-09 created."

echo "Done."
