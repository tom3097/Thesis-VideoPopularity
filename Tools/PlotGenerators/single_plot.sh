#!/bin/bash

# executing script which extracts data from caffe log
./parselog.sh $1

# creating script that will split train log file into several files
# based on learning rate value
printf "{ print > \$4\".lr\" }" > spl.sh

# executing script
awk -f spl.sh $1.train

# cleaning after script execution
rm spl.sh
rm TrainingLoss.lr

# creating script for Loss and Iterations plot
printf "reset\n" > plotgen1.gps
printf "set terminal png\n" >> plotgen1.gps 
printf "set output \"LossVsIterationsTrain.png\" \n" >> plotgen1.gps
printf "set style data lines\n" >> plotgen1.gps
printf "set key right\n" >> plotgen1.gps
printf "set title \"Training loss vs. training iterations\"\n" >> plotgen1.gps
printf "set ylabel \"Training loss\"\n" >> plotgen1.gps
printf "set xlabel \"Training iterations\"\n" >> plotgen1.gps
printf "plot " >> plotgen1.gps

flag=false

dirlist=(`ls *.lr | grep -v e`)
for ((i=${#dirlist[@]}-1; i>=0; i--));
do
    if $flag ; then
        printf ", " >> plotgen1.gps
    fi
    flag=true
    printf "\"${dirlist[$i]}\" " >> plotgen1.gps
    bname=$(basename "${dirlist[$i]}")
    title="${bname%.*}"
    printf "using 1:3 title \"Base lr=$title\"" >> plotgen1.gps
done

dirlist=(`ls *.lr | grep e`)

for ((i=0; i<${#dirlist[@]}; i++));
do
    if $flag ; then
        printf ", " >> plotgen1.gps
    fi
    flag=true
    printf "\"${dirlist[$i]}\" " >> plotgen1.gps
    bname=$(basename "${dirlist[$i]}")
    title="${bname%.*}"
    printf "using 1:3 title \"Base lr=$title\"" >> plotgen1.gps
done

# executing script
gnuplot plotgen1.gps

# cleaning after script execution
rm plotgen1.gps
rm *.lr

# creating script for Accuracy and Iterations plot
printf "reset\n" > plotgen2.gps
printf "set terminal png\n" >> plotgen2.gps 
printf "set output \"AccuracyVsIterationsTest.png\" \n" >> plotgen2.gps
printf "set style data lines\n" >> plotgen2.gps
printf "set key right\n" >> plotgen2.gps
printf "set title \"Testing accuracy vs. testing iterations\"\n" >> plotgen2.gps
printf "set ylabel \"Testing accuracy\"\n" >> plotgen2.gps
printf "set xlabel \"Testing iterations\"\n" >> plotgen2.gps
printf "plot \"$1.test\" using 1:3 title \"Accuracy\"" >> plotgen2.gps

# executing script
gnuplot plotgen2.gps

# cleaning after script execution
rm plotgen2.gps

# creating script for Loss and Iterations plot
printf "reset\n" > plotgen3.gps
printf "set terminal png\n" >> plotgen3.gps 
printf "set output \"LossVsIterationsTest.png\" \n" >> plotgen3.gps
printf "set style data lines\n" >> plotgen3.gps
printf "set key right\n" >> plotgen3.gps
printf "set title \"Testing loss vs. testing iterations\"\n" >> plotgen3.gps
printf "set ylabel \"Testing loss\"\n" >> plotgen3.gps
printf "set xlabel \"Testing iterations\"\n" >> plotgen3.gps
printf "plot \"$1.test\" using 1:4 title \"Loss\"" >> plotgen3.gps

# executing script
gnuplot plotgen3.gps

# cleaning after script execution
rm plotgen3.gps
