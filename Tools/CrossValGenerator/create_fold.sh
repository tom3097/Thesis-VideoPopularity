#!/bin/bash

# split train file into several files
./split_train.py $1 $2

end="$(($2-1))"

# create train and val files
for i in $(eval echo {0..$end})
do
    train_name="$1.$i"
    test_name="$3.$i"
    printf "" > "$test_name"
    printf "" > "$train_name"
    for j in $(eval echo {0..$end})
    do
        if [ "$j" == "$i" ]; then
            cat "group$j.txt" > "$test_name"
        else
            cat "group$j.txt" >> "$train_name"
        fi
    done
    cat "$3" >> "$train_name"
done

rm group*.txt
