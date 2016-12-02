## Cross Validatin Data Generator

Those scripts are used for creating all missing train.txt and val.txt files which are needed to perform cross validation. Sample train.txt and val.txt files needs to be generated before.

## Usage

Just type:

<code>./create_fold.sh TRAIN_FILE SPLIT_NUMBER VAL_FILE</code>

Where:
* TRAIN_FILE - train.txt file created with TrainValGenerator
* SPLIT_NUMBER - number of groups that train.txt file should be splitted into
* VAL_FILE - val.txt file created with TrainValGenerator

## Output

Train and val files are created, the number of files depends on the SPLIT_NUMBER argument.
