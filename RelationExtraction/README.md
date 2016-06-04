# RelationshipExtraction
This repository contains CMPE561 Course HW3 project. The project aims to implement a protein protein relationship extraction using machine learning methods.
## Requirements
The project is implemented in Python programming language. Python2.7 is required to run the code. (Neither Python3.x nor Python2.6 cannot run the code.)

scikit-learn Python package is required to run the app.
 * NumPy (>= 1.6.1),
 * SciPy (>= 0.9).
 * Scikit-learn (0.17.1)

All the requirements can be installed via this command:
```sh
pip install -U numpy scipy scikit-learn
```

Note: Please refer to [Scikit-learn installation details page](http://scikit-learn.org/stable/developers/advanced_installation.html) if you have any problems with installation.

## Dataset
In this homework, given dataset is used for both training and testing. First 3000 documents of all (4056) is used for training. The rest is used for testing.

Dataset files are included in this repository. Please put them in an appropriate place and note the path of dataset directory. 

### Description of Files
There are 2 .py files and a .java in the repository:
* app-base.py : This is a Python a script which trains an SVM with BoW-TFIDF approach. It does not use any extra features.

* app-advanced.py : A Python script which includes 2 extra sets of features: 1. Interaction verbs as binary features, 2. Features extracted using Stanford Dependency parser. Dependency parser features are extracted using app.java and saved into "dep_parsed.sentences" file before running app-advanced.py 

* app.java : A Java application to parse a dependency tree using Stanford Parser.

### How to run
First, clone the repository:

```sh
git clone git@github.com:sametatdag/CMPE561.git
cd CMPE561/RelationExtraction
```

Then run the app-base.py from command line Python interpreter:
```
$ python2.7 app-base.py
```

Run app-advanced.py from command line Python interpreter:
```
$ python2.7 app-advanded.py
```


If you want to re-extract dependency trees, you need to run app.java. To run app.java, you need to install Stanford Dependency Parser and English model as dependencies:

 * Create a new Java project in your Java IDE.
 * Import app.java file into your project.
 * Download [Stanford Dependency Tree parser](http://nlp.stanford.edu/software/stanford-parser-full-2015-12-09.zip)
 * Unzip stanford-parser-full-2015-12-09.zip file and add jars into your project as lib dependencies.
 * Download [English model files required for Stanford Parser](http://nlp.stanford.edu/software/stanford-english-corenlp-2016-01-10-models.jar)
 * Add models.jar into your project as lib dependencies.
 * Edit accordingly taggerPath and br paths in app.java with proper paths.
 * Run the project.
 * It will create a file including dependency parse tree features, named as dep_parsed.sentences.


### File Paths
If you encounter a path related problem, below is given all the variables carrying paths:
 * app-base.py:L10 sentences_file = "dataset/dataset.sentences"
 * app-base.py:L11 labels_file = "dataset/dataset.labels"

 * app-advanded.py:L25 dep_parsed_filename = "dep_parsed.sentences"
 * app-advanded.py:L42 sentences_file = "dataset/dataset.sentences"
 * app-advanded.py:L43 labels_file = "dataset/dataset.labels"
 * app-advanded.py:L44 keywords_file = "int-keywords.txt"

### Issues
If you encounter any error, please report an issue on Github.
