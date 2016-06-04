import sys
import numpy as np
from sklearn import svm
from random import shuffle
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer

# Given dataset files. "dataset" directory should be in the 
# same directory with app-base.py file.
sentences_file = "dataset/dataset.sentences"
labels_file = "dataset/dataset.labels"

# Read sentences and labels into lists. (Omit last line, since it's empty.)
sentences = open(sentences_file,'r').read().split('\n')
sentences = sentences[:-1]
labels = open(labels_file,'r').read().split('\n')

labels = labels[:-1]

# Convert labels to integers.
labels = [int(l) for l in labels]

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
tfidf_vectorizer = TfidfVectorizer(min_df=200,
                             max_df = 0.4,
                             sublinear_tf=True,
                             use_idf=True)

# convert train and test sets into feature vectors.
X_train_features = tfidf_vectorizer.fit_transform(train_data)
X_test_features = tfidf_vectorizer.transform(test_data)


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
