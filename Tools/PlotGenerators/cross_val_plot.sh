#!/bin/bash

# creating script for Accuracy and Iterations plot
printf "reset\n" > plotgen1.gps
printf "set terminal png\n" >> plotgen1.gps 
printf "set output \"AccuracyVsIterationsTest.png\" \n" >> plotgen1.gps
printf "set style data lines\n" >> plotgen1.gps
printf "set key right\n" >> plotgen1.gps
printf "set title \"Testing accuracy vs. testing iterations\"\n" >> plotgen1.gps
printf "set ylabel \"Testing accuracy\"\n" >> plotgen1.gps
printf "set xlabel \"Testing iterations\"\n" >> plotgen1.gps
printf "plot " >> plotgen1.gps

# creating script for Loss and Iterations plot
printf "reset\n" > plotgen2.gps
printf "set terminal png\n" >> plotgen2.gps 
printf "set output \"LossVsIterationsTest.png\" \n" >> plotgen2.gps
printf "set style data lines\n" >> plotgen2.gps
printf "set key right\n" >> plotgen2.gps
printf "set title \"Testing loss vs. testing iterations\"\n" >> plotgen2.gps
printf "set ylabel \"Testing loss\"\n" >> plotgen2.gps
printf "set xlabel \"Testing iterations\"\n" >> plotgen2.gps
printf "plot " >> plotgen2.gps

flag=false

dirlist=(`ls $1*`)

for ((i=0; i<${#dirlist[@]}; i++));
do
    # executing script which extracts data from caffe log
    ./parselog.sh "${dirlist[$i]}"
    if $flag ; then
        printf ", " >> plotgen1.gps
        printf ", " >> plotgen2.gps
    fi
    flag=true
    printf "\"${dirlist[$i]}.test\" " >> plotgen1.gps
    printf "\"${dirlist[$i]}.test\" " >> plotgen2.gps
    title="${dirlist[$i]}"
    printf "using 1:3 title \"$title\"" >> plotgen1.gps
    printf "using 1:4 title \"$title\"" >> plotgen2.gps
done

# executing script
gnuplot plotgen1.gps
gnuplot plotgen2.gps

# cleaning after script execution
rm plotgen1.gps
rm *.test
rm *.train
