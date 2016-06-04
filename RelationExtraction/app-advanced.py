import sys
import numpy as np
from sklearn import svm
from scipy import sparse
from random import shuffle
from sklearn import metrics
from sklearn.pipeline import FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


## This is a custom vectorizer. It reads dependency parsed dataset
## from a given dataset file. In the dep_parsed.sentences, 
## each line contains a sentence with a value of 0 or 1.
## This is a binary feature that is set if the total distance of 
## both protein names to an interaction verb in a sentence is 2,
## that is, if both protein names are the immediate children 
## of an interaction verb.
class DependencyVectorizer(BaseEstimator, TransformerMixin):
  def fit(self, x, y=None):
    return self
  
  def transform(self, documents):
    dep_parsed_filename = "dep_parsed.sentences"
    dep_parsed = open(dep_parsed_filename,'r').read().split('\n')[:-1]
    parsed = {}

    for s in dep_parsed:
      parts = s.split("|||")
      s_key = parts[0]
      s_val = parts[1]
      parsed[s_key] = int(s_val)

    features = [[parsed.get(d, 0)] for d in documents]
    result = sparse.csr_matrix(np.array(features))
    return result
## End of custom vectorizer

# Given dataset files. "dataset" directory should be in the
# same directory with app-base.py file.
sentences_file = "dataset/dataset.sentences"
labels_file = "dataset/dataset.labels"
keywords_file = "int-keywords.txt"

# Read sentences and labels into lists. (Omit last line, since it's empty.)
sentences = open(sentences_file,'r').read().split('\n')
sentences = sentences[:-1]
labels = open(labels_file,'r').read().split('\n')

labels = labels[:-1]

# Convert labels to integers.
labels = [int(l) for l in labels]

keywords = open(keywords_file,'r').read().split('\n')
keywords = keywords[:-1]

print("Shuffling the documents...")
# shuffle the dataset, since first 3000 items mostly belong to same class.
indices = range(len(sentences))
shuffle(indices)


# split train and test sets.
train_indices = indices[:3000]
test_indices = indices[3000:]

train_data = []
train_labels = []
test_data = []
test_labels = []

for i in train_indices:
  train_data.append(sentences[i])
  train_labels.append(labels[i])

for i in test_indices:
  test_data.append(sentences[i])
  test_labels.append(labels[i])
## end of splitting.

print "Train and test sets are ready."
print("Training set contains %s documents." % len(train_data))
print("Test set contains %s documents.\n" % len(test_data))

# Count Tf-idf values using Scikit Learn TfidfVectorizer.
tfidf_vectorizer = TfidfVectorizer(min_df=100,
                             max_df = 0.4,
                             sublinear_tf=True,
                             use_idf=True)


print("Adding interaction verbs to feature vectors...\n")
## This vectorizer prepares each interaction word in our 
## list is a binary feature by itself. In other words, 
## if a particular interaction wordoccurs in a sentence, 
## we set the corresponding feature for that sentence. 
count_vectorizer = CountVectorizer(vocabulary=keywords)

print("Adding dependency parse tree distance feature to feature vectors...\n")
## Custom vectorizer to append additional feature. 
## Please refer to the comment at the top of the class definition
## of DependencyVectorizer for details.
dependency_vectorizer = DependencyVectorizer()


## Combine Tfidf features, interaction word binary features and Dependency 
## word features.
unioned_features = FeatureUnion(
        [('tfidf', tfidf_vectorizer), ('external_features', count_vectorizer), ('stats', dependency_vectorizer)])

# convert train and test sets into feature vectors.
X_train_features = unioned_features.fit_transform(train_data)
X_test_features = unioned_features.transform(test_data)


# Prepare a linear kernel SVM
classifier_linear = svm.SVC(kernel='linear')
print "SVM is ready."

# Train SVM over training data.
classifier_linear.fit(X_train_features, train_labels)
print "SVM training completed."

# Predict the test data.
prediction_linear = classifier_linear.predict(X_test_features)
print "Prediction is completed."

print "\nCalculating average accuracy with 10 runs..."

# Run 10 times, take average of accuracy.
total = 0
for i in range(10):
  accuracy = classifier_linear.score(X_test_features, test_labels)
  total += accuracy
accuracy = total / 10
print("\nAccuracy: %s\n" % accuracy)

# Print performance evaluation.
print(metrics.classification_report(test_labels, prediction_linear))
