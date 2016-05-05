#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import codecs
from decimal import Decimal
from json import load
from TagWord import TagWord


postag_required = False
tag_index = 3 # CPOSTAG

if postag_required:
  tag_index = 4  # POSTAG

pos_tags = [
  "START",
  "Adv", "Punc", "Noun",
  "Adj", "Verb", "Det",
  "Pron", "Postp", "Conj",
  "Ques", "Num", "Interj",
  "Dup", "Zero",
  "END"
]

def remove_newlines(text):
  return text.replace("\n", "")

def decimal_default(obj):
  if isinstance(obj, Decimal):
    return float(obj)
  raise TypeError

backtrace = {}
def process_sentence(sentence):

  for tagword in sentence:
    word = tagword.word
    for q in pos_tags:
      if word == "START":
        prob = 1.0
      elif word == "END":
        prob = 100.0
      else:
        prob = 0.0
      key = word + "|" + q
      backtrace[key] = {"prob": prob, "prev": None}

  prev_word = "START".encode('utf-8')
  for w in sentence:
    word = w.word
    if word in [ "START"]:
      pass
    else:
      for q in pos_tags:
        column_probs = []
        backlinks = []
        for q0 in pos_tags:
          if q0 in ["START", "END"]:
            continue
          else:
            key1 = prev_word + "|" + q0
            back_prob = backtrace[key1].get("prob")
            key2 = q0 + "|" + q
            tag_trans_prob = tag_transitions.get(key2, 0.0)
            key3 = q + "|" + word
            if word in observation_likelihoods and  q in observation_likelihoods.get(word):
              obs_prob = observation_likelihoods.get(word).get(q)
            else:
              obs_prob = 0.0
            column_probs.append(back_prob * tag_trans_prob)
            backlinks.append(q0)
        most_probable_tag = backlinks[column_probs.index(max(column_probs))]
        highest_probability = max(column_probs)
        backtrace[word + "|" + q]["prob"] = highest_probability
        backtrace[word + "|" + q]["prev"] = most_probable_tag
      prev_word = word

  s = []
  tag = "END"
  for i in range(len(sentence)-1, -1, -1):
    word = sentence[i].word
    true_tag = sentence[i].tag
    # print word, tag
    r = {"word":word , "tag": tag, "true_tag": true_tag}
    s.insert(0, r)
    key = word + "|" + tag
    tag = backtrace.get(key).get("prev")

  return s

def usage():
  print "\nUsage: /usr/bin/python2.7 hmm_tagger.py --test-filename <test filename> --output-filename <output filename>\n"

try:
  opts, args = getopt.getopt(sys.argv[1:], 't:o:h', ['test-filename=', 'output-filename='])
  if len(opts) < 2:
    usage()
    sys.exit(2)
except getopt.GetoptError as e:
  usage()
  sys.exit(2)

for opt, arg in opts:
  if opt in ('-h', '--help'):
    usage()
    sys.exit(2)
  elif opt in ('-t', '--test-filename'):
    test_filename = arg
  elif opt in ('-p', '--output-filename'):
    output_filename = arg
  else:
    usage()
    sys.exit(2)



with open('tag_transitions.txt', "r") as f:    
  tag_transitions = load(f)

with open('observation_likelihoods.txt', "r") as f:    
  observation_likelihoods = load(f)

sentence = []

with codecs.open(output_filename, "w", "utf-8") as f:

  for i in codecs.open(test_filename, encoding="utf-8").readlines():
    if i == "\n":
      start_tagword = TagWord("START", "START")
      end_tagword = TagWord("END", "END")

      sentence.insert(0, start_tagword)
      sentence.append(end_tagword)

      result = process_sentence(sentence)

      for w in result:
        f.write("%s\t%s\t%s\n" % (w.get("word"), w.get("tag"), w.get("true_tag")))
      f.write("\n")
      sentence = []
    else:
      line = remove_newlines(i)
      parsed = line.split("\t")

      line = remove_newlines(i)
      parsed = line.split("\t")

      word = parsed[1]
      tag = parsed[tag_index]

      tagword = TagWord(tag, word)
      sentence.append(tagword)