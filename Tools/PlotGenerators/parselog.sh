#!/bin/bash
# Usage parselog.sh caffe.log 
# It creates two files one caffe.log.test that contains the loss and test accuracy of the test and
# another one caffe.log.loss that contains the loss computed during the training

if [ "$#" -lt 1 ]
then
echo "Usage parselog.sh /path/to/your.log"
exit
fi

LOG=`basename $1`
grep -v 'Data layer prefetch queue empty' $1 > filt1.txt
grep -v 'Waiting for data' filt1.txt > filt2.txt
grep -B 1 'Test ' filt2.txt > aux.txt
grep 'Iteration ' aux.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > aux0.txt
grep 'Test net output #0' aux.txt | awk '{print $11}' > aux1.txt
grep 'Test net output #1' aux.txt | awk '{print $11}' > aux2.txt

# Extracting elpased seconds
# For extraction of time since this line constains the start time
grep '] Solving ' $1 > aux3.txt
grep 'Testing net' $1 >> aux3.txt
./extract_seconds.py aux3.txt aux4.txt

# Generating
echo '# Iters Seconds TestAccuracy TestLoss'> $LOG.test
paste aux0.txt aux4.txt aux1.txt aux2.txt | column -t >> $LOG.test
rm aux.txt aux0.txt aux1.txt aux2.txt aux3.txt aux4.txt

# For extraction of time since this line constains the start time
grep '] Solving ' $1 > aux.txt
grep ', loss = ' $1 >> aux.txt
grep 'Iteration ' aux.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > aux0.txt
grep ', loss = ' $1 | awk '{print $9}' > aux1.txt
grep ', lr = ' $1 | awk '{print $9}' > aux2.txt

# Extracting elpased seconds
./extract_seconds.py aux.txt aux3.txt

# Generating
echo '# Iters Seconds TrainingLoss LearningRate'> $LOG.train
paste aux0.txt aux3.txt aux1.txt aux2.txt | column -t >> $LOG.train
rm filt1.txt filt2.txt aux.txt aux0.txt aux1.txt aux2.txt aux3.txt
