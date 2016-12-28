TOOLS=../../caffe/build/tools

export HDF5_DISABLE_VERSION_CHECK=1
export PYTHONPATH=.

$TOOLS/caffe test -model train_test_frames_LSTM.prototxt -weights snapshots_frames_LSTM_iter_30000.caffemodel -gpu 0 -iterations 3240
