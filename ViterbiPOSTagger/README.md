# ViterbiPOSTagger
This repository contains CMPE561 Course HW2 project. The project aims to implement a HMM Part-of-Speech Tagger with using Viterbi Decoding..
## Requirements
The project is implemented in Python programming language. Python2.7 is required to run the code. (Wither Python3.x or Python2.6 cannot run the code.)

No external libraries required. 

## Dataset
HMM is trained on a labeled data so that a labeled dataset is necessary. In this homework, the dataset below is used:
* Training: turkish_metu_sabanci_train.conll
* Validation: turkish_metu_sabanci_val.conll

Both files are included in this repository. Please put them in an appropriate place and note the path of dataset directory. 

### Description of Files
There are 3 .py files in the repository:
* train_hmm_tagger.py : This is a Python a script which takes "training_file" and Part-of-Speech tagset (cpostag or postag) as arguments and trains the tagger.

* hmm_tagger.py : A Python script which takes "test_file" and "output_file" as arguments and tags the unseen test data and writes the computed tags into output file.

* evaluate_hmm_tagger.py : A Python script which takes "output_file" and "gold file" as arguments and compares the output of the implemented tagger with the gold standard for the test data.

### How to run
First, clone the repository:

```sh
git clone git@github.com:sametatdag/CMPE561.git
cd CMPE561/ViterbiPOSTagger
```

Then run the train_hmm_tagger from command line Python interpreter:
for postag type:
```
$ python2.7 train_hmm_tagger.py --training-filename turkish_metu_sabanci_train.conll --postag-type **postag**
```
or for cpostag type:
```
$ python2.7 train_hmm_tagger.py --training-filename turkish_metu_sabanci_train.conll --postag-type **cpostag**
```
train_hmm_tagger.py will create two new files: observation_likelihoods.txt and tag_transitions.txt. These file contains the training parameters of the HMM in JSON format. Please do not delete them, these two files are required for running step 2.


Next, you need to run the actual tagger, again from command line:
```
$ python2.7 hmm_tagger.py --test-filename turkish_metu_sabanci_val.conll --output-filename output.txt
```
When hmm_tagger.py finished running, it creates an output file with the given name, e.g. in this example; output.txt. output.txt contains 3-column data: word, estimated_tag, true_tag. (This is slightly different then the requirements of the homework, since in this structure, we already have the gold standard in output.txt file.)

For evaluation of the results, the next step is running the evaluator script:
```
$ python2.7 evaluate_hmm_tagger.py --output-filename hede.txt
```
evaluate_hmm_tagger.py prints out 2 types of information:
* Overall accuracy
* Confusion matrix.

### Issues
If you encounter any error, please report an issue on Github.
