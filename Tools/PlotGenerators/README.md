## Plot generators

Those scripts are used for generating plots based on logs from caffe (logs from training).

## Usage

To use this script just type

<code>./plot.sh logs_from_training.txt</code>

where logs_from_training.txt is the output printed to the screan while training. Output can be saved with <code>| tee logs_from_training.txt</code> command.

## Output

Three files will be created:
 * Test Accurancy vs. Test Iteration plot
 * Test Loss vs. Test Iteration plot
 * Train Loss vs. Train Iterations plot (different colors refers to different learning rates)
