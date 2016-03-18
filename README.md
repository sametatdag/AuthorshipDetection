# AuthorshipDetection
This repository contains CMPE561 Course HW1 project. The project aims to implement a Naive Bayes Classifier to predict the author of a given document.
## Requirements
The project is implemented in Python programming language. Python2.7 is required to run the code. (Python2.6 cannot run the code.)

No external libraries required. 

## Dataset
69 Authors dataset is required. Please download and unzip the dataset in an appropriate place and note the path of dataset directory. 

For Function Words, fWords.txt from text2arff.zip file is required. Please download that file as well.

### Description of Files
There are two .py files in the repository:
* build_test_and_training_sets.py : Creates training and test set directories. Randomly chooses 60% of files for every author in the original dataset, copies those into training dataset; copies the rest (40%) to the test dataset.

* recognize_and_evaluate.py : Trains a Naive Bayes classifier using training set. Tests the classifier using test set. Evaluates and prints the results.
### How to run
First, clone the repository:

```sh
git clone https://github.com/sametatdag/AuthorshipDetection.git
cd AuthorshipDetection
```

Then run the training-test set builder from command line Python interpreter:
```
$ python2.7 build_test_and_training_sets.py --data-set /tmp/raw_texts --training-set /tmp/train/ --test-set /tmp/test/
```

Next, you need to run the actual recognizer, again from command line:
```
$ python2.7 recognize_and_evaluate.py --training-set /tmp/train/ --test-set /tmp/test --use-function-words True --f-words-path /tmp/fWords.txt 
```
If you do not want to use the function words, you can use the parameter like this: ```--use-function-words False```.

### Issues
If you encounter any error, please report an issue on Github.
