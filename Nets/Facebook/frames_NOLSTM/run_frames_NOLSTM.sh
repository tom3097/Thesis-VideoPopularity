#!/bin/sh
TOOLS=../../caffe/build/tools

echo 'Frames NOLSTM started.'
GLOG_logtostderr=1 $TOOLS/caffe train -solver frames_NOLSTM_solver.prototxt -weights ../../caffe_imagenet_hyb2_wr_rc_solver_sqrt_iter_310000 2>&1 | tee frames_NOLSTM.txt
echo 'Done.'
