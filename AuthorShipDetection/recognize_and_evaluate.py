import os
import re
import sys
import math
import getopt
import string

###
# Utility Functions
##

def remove_punctuation(s):
    table = string.maketrans("", "")
    return s.translate(table, string.punctuation)


def tokenize(long_text):
    long_text = remove_punctuation(long_text)
    long_text = long_text.lower()
    return re.compile("\W+", re.UNICODE).split(long_text)


def count_words(all_words):
    wc = {}
    for wword in all_words:
        wc[wword] = wc.get(wword, 0.0) + 1.0
    return wc

###
# End of Utility Functions
##






def usage():
    print "\nUsage: /usr/bin/python2.7 recognize_and_evaluate.py " \
          "--training-set /path/to/training/set \n --test-set /path/to/test/set " \
          "--use-function-words=[True|False] --f-words-path /path/to/functionwords.txt \n"

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:t:u:f:h',
                               ['training-set=', 'test-set=', 'use-function-words=', 'f-words-path='])
    if len(opts) < 4:
        usage()
        sys.exit(2)
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-i', '--training-set'):
        train_dir = arg
    elif opt in ('-t', '--test-set'):
        test_dir = arg
    elif opt in ('-u', '--use-function-words'):
        use_fwords = bool(arg)
    elif opt in ('-f', '--f-words-path'):
        fwords_path = arg
    else:
        usage()
        sys.exit(2)

use_fwords = False
fwords_path = "/Users/samet/Documents/workspace/NLP/hw1/fWords.txt"

# Initializing necessary data structues
vocab = {}
word_counts = {}
priors = {}
docs = []

sub_dirs = [name for name in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, name))]

if use_fwords:
    text = open(fwords_path).read()
    fwords = tokenize(text)
    print fwords


##
# Training phase
##
for author in sub_dirs:
    author_path = os.path.join(train_dir, author)
    author_files = os.listdir(author_path)

    priors[author] = 0.
    if use_fwords:
        word_counts[author] = dict.fromkeys(fwords, 1.0)
    else:
        word_counts[author] = {}

    for f in author_files:

        if f == ".DS_Store":
            continue

        f = os.path.join(author_path, f)

        docs.append((author, f))

        priors[author] += 1
        text = open(f).read()
        words = tokenize(text)
        counts = count_words(words)

        for word, count in counts.items():
            if len(word) <= 3:
                continue


            if word not in vocab:
                vocab[word] = 0.0
            if word not in word_counts[author]:
                word_counts[author][word] = 0.0

            vocab[word] += count
            word_counts[author][word] += count

##
# End of Training phase
##



##
# Test phase
##

denominators = {}
for p in sub_dirs:
    denominators[p] = sum(word_counts[p].values()) + len(vocab.keys())

sub_dirs = [name for name in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, name))]

pc = {}
for p in sub_dirs:
    pc[p] = priors[p] / sum(priors.values())

contingencies = {}
for p in sub_dirs:
    contingencies[p] = {}
    contingencies[p]["YY"] = 0.0
    contingencies[p]["YN"] = 0.0
    contingencies[p]["NY"] = 0.0

for author in sub_dirs:

    # print author
    author_path = os.path.join(test_dir, author)
    author_files = os.listdir(author_path)
    counts = {}

    for f in author_files:

        if f == ".DS_Store":
            continue

        filepath = os.path.join(author_path, f)

        text = open(filepath).read()
        words = tokenize(text)
        t_counts = count_words(words)

        for t_word, t_count in t_counts.items():
            if t_word not in counts:
                counts[t_word] = 0.0
            counts[t_word] += t_count
            # --> At this step, we have an author's single text file counts.

        # initialize log probabilities
        log_probabilities = {}
        for p in sub_dirs:
            log_probabilities[p] = 1.0

        p_w_given = {}

        for w, cnt in list(counts.items()):

            if w not in vocab or len(w) <= 3:
                continue

            for p in sub_dirs:
                p_w_given[p] = word_counts[p].get(w, 1.0) / denominators[p]
                if p_w_given[p] == 0:
                    print word_counts[p].get(w, 1.0)
                    print denominators[p]

            for p in sub_dirs:
                log_probabilities[p] += math.log(cnt * p_w_given[p])

        for p in sub_dirs:
            log_probabilities[p] += math.log(pc[p])

        pred = max(log_probabilities, key=log_probabilities.get)

        print("File: {}, Actual:  {}  Predicted: {}".format(f, author, pred))

        for p_author in sub_dirs:
            if author == p_author:
                if author == pred:
                    contingencies[p_author]["YY"] += 1.0
                else:
                    contingencies[p_author]["NY"] += 1.0
            else:
                if author == pred:
                    contingencies[p_author]["YN"] += 1.0

##
# End of Test phase
##


##
# Evaluation phase
##

total_precision = 0.0
total_recall = 0.0
total_f1 = 0.0

for author in contingencies.keys():
    precision = contingencies[author]["YY"] / (contingencies[author]["YY"] + contingencies[author]["YN"])
    total_precision += precision

    recall = contingencies[author]["YY"] / (contingencies[author]["YY"] + contingencies[author]["NY"])
    total_recall += recall

    if (precision + recall) > 0:
        f1 = (2 * precision * recall) / (precision + recall)
        total_f1 += f1


macro_precision = total_precision / len(contingencies.keys())
macro_recall = total_recall / len(contingencies.keys())
macro_f1 = total_f1 / len(contingencies.keys())

print("\n--------------Results--------------")

print("macro averages --> precision: {}, recall: {}, f1: {}".format(macro_precision, macro_recall, macro_f1))


micro_contingencies = {}
micro_contingencies["YY"] = 0.0
micro_contingencies["YN"] = 0.0
micro_contingencies["NY"] = 0.0


for p in contingencies.keys():
    micro_contingencies["YY"] += contingencies[p]["YY"]
    micro_contingencies["YN"] += contingencies[p]["YN"]
    micro_contingencies["NY"] += contingencies[p]["NY"]


micro_precision = micro_contingencies["YY"] / (micro_contingencies["YY"] + micro_contingencies["YN"])
micro_recall = micro_contingencies["YY"] / (micro_contingencies["YY"] + micro_contingencies["NY"])
micro_f1 = (2 * micro_precision * micro_recall) / (micro_precision + micro_recall)

print("\nmicro averages --> precision: {}, recall: {}, f1: {}".format(micro_precision, micro_recall, micro_f1))

##
# End of Evaluation phase
##