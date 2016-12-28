#!/bin/bash

TOOLS=../../caffe/build/tools

export HDF5_DISABLE_VERSION_CHECK=1
export PYTHONPATH=.

GLOG_logtostderr=1  $TOOLS/caffe train -solver frames_LSTM_solver.prototxt -weights ../binary/snapshots_frames_NOLSTM_iter_5000.caffemodel 2>&1 | tee logsi_asas.log
echo "Done."

